from flask import Blueprint, request, current_app, jsonify, send_file
from models import Country, Meta
from db import db
from services.refresh_service import refresh_all
from utils.errors import bad_request, not_found, internal_error, external_unavailable
from utils.validators import validate_country_payload
from sqlalchemy import desc

countries_bp = Blueprint("countries", __name__)

@countries_bp.route("/refresh", methods=["POST"])
def refresh():
    result = refresh_all()
    if result is None:
        return external_unavailable("Unknown API")
    if result.get("error"):
        if result["api"] == "Countries API":
            return external_unavailable("Countries API")
        if result["api"] == "Exchange API":
            return external_unavailable("Exchange API")
        return internal_error()
    return jsonify({"message": "Data refreshed", "total": result.get("total", 0)}), 200

@countries_bp.route("", methods=["GET"])
def list_countries():
    q = Country.query
    region = request.args.get("region")
    currency = request.args.get("currency")
    sort = request.args.get("sort")  # gdp_desc etc.
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 100))

    if region:
        q = q.filter(Country.region == region)
    if currency:
        q = q.filter(Country.currency_code == currency)

    if sort:
        if sort == "gdp_desc":
            q = q.order_by(Country.estimated_gdp.desc().nullslast())
        elif sort == "gdp_asc":
            q = q.order_by(Country.estimated_gdp.asc().nullslast())
        elif sort == "population_desc":
            q = q.order_by(Country.population.desc())
        elif sort == "population_asc":
            q = q.order_by(Country.population.asc())

    pagination = q.paginate(page=page, per_page=per_page, error_out=False)
    items = [c.to_dict() for c in pagination.items]
    return jsonify(items), 200

@countries_bp.route("/<string:name>", methods=["GET"])
def get_country(name):
    c = Country.query.filter(Country.name.ilike(name)).first()
    if not c:
        return not_found()
    return jsonify(c.to_dict()), 200

@countries_bp.route("/<string:name>", methods=["DELETE"])
def delete_country(name):
    c = Country.query.filter(Country.name.ilike(name)).first()
    if not c:
        return not_found()
    try:
        db.session.delete(c)
        db.session.commit()
        return jsonify({"message": "Deleted"}), 200
    except Exception:
        db.session.rollback()
        return internal_error()

@countries_bp.route("/image", methods=["GET"])
def get_image():
    import os
    from config import Config
    path = os.path.join(Config.CACHE_DIR, "summary.png")
    if not os.path.exists(path):
        return jsonify({"error": "Summary image not found"}), 404
    return send_file(path, mimetype="image/png")

