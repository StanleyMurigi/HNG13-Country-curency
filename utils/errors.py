from flask import jsonify

def bad_request(details=None):
    payload = {"error": "Validation failed"}
    if details:
        payload["details"] = details
    return jsonify(payload), 400

def not_found():
    return jsonify({"error": "Country not found"}), 404

def internal_error():
    return jsonify({"error": "Internal server error"}), 500

def external_unavailable(api_name):
    return jsonify({"error": "External data source unavailable", "details": f"Could not fetch data from {api_name}"}), 503

