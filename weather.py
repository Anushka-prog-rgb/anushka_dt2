from flask import Blueprint, request, jsonify

weather_bp = Blueprint("weather", __name__)

# Mock database / data
MOCK_CURRENT = {
    "London": {"temperature": 12, "condition": "Cloudy", "humidity": 81},
    "Paris": {"temperature": 16, "condition": "Sunny", "humidity": 60},
    "New York": {"temperature": 8, "condition": "Rain", "humidity": 90},
}

MOCK_FORECAST = {
    "Paris": [
        {"day": "Day 1", "temperature": 16, "condition": "Sunny", "humidity": 60},
        {"day": "Day 2", "temperature": 15, "condition": "Partly Cloudy", "humidity": 65},
        {"day": "Day 3", "temperature": 14, "condition": "Light Rain", "humidity": 70},
        {"day": "Day 4", "temperature": 13, "condition": "Cloudy", "humidity": 75},
    ],
    "London": [
        {"day": "Day 1", "temperature": 12, "condition": "Cloudy", "humidity": 81},
        {"day": "Day 2", "temperature": 11, "condition": "Rain", "humidity": 85},
        {"day": "Day 3", "temperature": 13, "condition": "Cloudy", "humidity": 80},
    ]
}

@weather_bp.route("/current")
def current_weather():
    # Example URL: /api/weather/current?city=London
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "Missing 'city' parameter"}), 400

    data = MOCK_CURRENT.get(city)
    if not data:
        return jsonify({"error": f"No data for city '{city}'"}), 404

    return jsonify({
        "city": city,
        "temperature": data["temperature"],
        "condition": data["condition"],
        "humidity": data["humidity"]
    })


@weather_bp.route("/forecast")
def forecast():
    # Example URL: /api/weather/forecast?city=Paris&days=3
    city = request.args.get("city", "").strip()
    days = request.args.get("days", "3")
    try:
        days = int(days)
    except ValueError:
        return jsonify({"error": "'days' must be an integer"}), 400

    if not city:
        return jsonify({"error": "Missing 'city' parameter"}), 400

    city_forecasts = MOCK_FORECAST.get(city)
    if not city_forecasts:
        return jsonify({"error": f"No forecast data for city '{city}'"}), 404

    # Return up to `days` items
    days = max(1, min(days, len(city_forecasts)))
    result = city_forecasts[:days]
    return jsonify({
        "city": city,
        "days": days,
        "forecast": result
    })
