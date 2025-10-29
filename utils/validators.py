def validate_country_payload(data):
    errors = {}
    if not data:
        errors["body"] = "Request body is required"
        return errors
    name = data.get("name")
    population = data.get("population")
    currency_code = data.get("currency_code")
    if not name:
        errors["name"] = "is required"
    if population is None:
        errors["population"] = "is required"
    else:
        try:
            pv = int(population)
            if pv < 0:
                errors["population"] = "must be >= 0"
        except Exception:
            errors["population"] = "must be an integer"
    if not currency_code:
        errors["currency_code"] = "is required"
    return errors

