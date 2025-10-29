from flask import Flask, jsonify
from config import Config
from db import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # register blueprint
    from routes.countries import countries_bp
    app.register_blueprint(countries_bp, url_prefix="/countries")

    # status endpoint at root /status
    @app.route("/status", methods=["GET"])
    def status():
        from models import Country, Meta
        total = Country.query.count()
        last_refresh = Meta.query.filter_by(key="last_refreshed_at").first()
        return jsonify({
            "total_countries": total,
            "last_refreshed_at": last_refresh.value if last_refresh else None
        })

    with app.app_context():
        # ensure cache dir
        os.makedirs(app.config.get("CACHE_DIR", "cache"), exist_ok=True)
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

