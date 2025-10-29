import random
from datetime import datetime
from db import db
from models import Country, Meta
from services.external_api import fetch_countries, fetch_exchange_rates
from services.image_service import generate_summary_image

def refresh_all():
    # 1) fetch external data
    countries_data = fetch_countries()
    if countries_data is None:
        return {"error": "countries_api_failed", "api": "Countries API"}

    rates = fetch_exchange_rates()
    if rates is None:
        return {"error": "exchange_api_failed", "api": "Exchange API"}

    # Build list of processed rows
    rows = []
    now = datetime.utcnow()
    for c in countries_data:
        name = c.get("name")
        capital = c.get("capital")
        region = c.get("region")
        population = c.get("population") or 0
        flag = c.get("flag")
        currencies = c.get("currencies") or []

        if not currencies:
            currency_code = None
            exchange_rate = None
            estimated_gdp = 0
        else:
            first = currencies[0]
            currency_code = first.get("code") if isinstance(first, dict) else None
            exchange_rate = None
            estimated_gdp = None
            if currency_code:
                # look up rate in rates map
                rate_val = rates.get(currency_code)
                if rate_val is not None:
                    exchange_rate = float(rate_val)
                    multiplier = random.randint(1000, 2000)
                    # avoid division by zero
                    try:
                        estimated_gdp = (population * multiplier) / exchange_rate if exchange_rate != 0 else None
                    except Exception:
                        estimated_gdp = None
                else:
                    exchange_rate = None
                    estimated_gdp = None

        rows.append({
            "name": name,
            "capital": capital,
            "region": region,
            "population": population,
            "currency_code": currency_code,
            "exchange_rate": exchange_rate,
            "estimated_gdp": estimated_gdp,
            "flag_url": flag,
            "last_refreshed_at": now
        })

    # 2) persist: make sure we do not modify DB if something goes wrong after fetching
    try:
        # Use a transaction
        with db.session.begin_nested():
            # Upsert by case-insensitive name
            for r in rows:
                # match by name case-insensitive
                existing = Country.query.filter(Country.name.ilike(r["name"])).first()
                if existing:
                    existing.capital = r["capital"]
                    existing.region = r["region"]
                    existing.population = int(r["population"]) if r["population"] is not None else 0
                    existing.currency_code = r["currency_code"]
                    existing.exchange_rate = r["exchange_rate"]
                    existing.estimated_gdp = r["estimated_gdp"]
                    existing.flag_url = r["flag_url"]
                    existing.last_refreshed_at = r["last_refreshed_at"]
                    db.session.add(existing)
                else:
                    new = Country(
                        name=r["name"],
                        capital=r["capital"],
                        region=r["region"],
                        population=int(r["population"]) if r["population"] is not None else 0,
                        currency_code=r["currency_code"],
                        exchange_rate=r["exchange_rate"],
                        estimated_gdp=r["estimated_gdp"],
                        flag_url=r["flag_url"],
                        last_refreshed_at=r["last_refreshed_at"]
                    )
                    db.session.add(new)

            # Update meta last_refreshed_at in same transaction
            meta = Meta.query.filter_by(key="last_refreshed_at").first()
            iso_now = now.isoformat() + "Z"
            if meta:
                meta.value = iso_now
            else:
                meta = Meta(key="last_refreshed_at", value=iso_now)
                db.session.add(meta)

            # flush to DB (but let outer commit happen)
            db.session.flush()

        # Commit top-level
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {"error": "db_commit_failed", "details": str(e)}

    # 3) generate image (best-effort; we will still return success even if image generation fails)
    try:
        total = Country.query.count()
        top5 = Country.query.filter(Country.estimated_gdp != None).order_by(Country.estimated_gdp.desc()).limit(5).all()
        top5_list = [{"name": c.name, "estimated_gdp": c.estimated_gdp, "flag_url": c.flag_url} for c in top5]
        last_ref_meta = Meta.query.filter_by(key="last_refreshed_at").first()
        last_ref = last_ref_meta.value if last_ref_meta else (datetime.utcnow().isoformat() + "Z")
        image_path = generate_summary_image(total, top5_list, last_ref)
    except Exception as e:
        # log in real app; here we swallow image generation errors
        image_path = None

    return {"success": True, "total": Country.query.count(), "image": image_path}

