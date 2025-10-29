from datetime import datetime
from db import db

class Country(db.Model):
    __tablename__ = "countries"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    capital = db.Column(db.String(200))
    region = db.Column(db.String(200))
    population = db.Column(db.Integer, nullable=False)
    currency_code = db.Column(db.String(10))
    exchange_rate = db.Column(db.Float)
    estimated_gdp = db.Column(db.Float)
    flag_url = db.Column(db.String(500))
    last_refreshed_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "capital": self.capital,
            "region": self.region,
            "population": self.population,
            "currency_code": self.currency_code,
            "exchange_rate": self.exchange_rate,
            "estimated_gdp": self.estimated_gdp,
            "flag_url": self.flag_url,
            "last_refreshed_at": self.last_refreshed_at.isoformat() + "Z" if self.last_refreshed_at else None
        }

class Meta(db.Model):
    __tablename__ = "meta"
    key = db.Column(db.String(100), primary_key=True)
    value = db.Column(db.String(500))

