import math

def compute_risk(weather, nitrogen, regional, growth, state_weight, monsoon_factor):

    humidity = weather.get("humidity", 50) / 100
    temp_index = weather.get("temp_index", 0.5)
    rain_index = weather.get("rain_streak_index", 0.5)

    weather_pressure = (
        0.35 * humidity +
        0.35 * rain_index +
        0.30 * temp_index
    )

    bio_pressure = (
        0.6 * nitrogen +
        0.4 * growth
    )

    base_score = (
        0.45 * weather_pressure +
        0.35 * bio_pressure +
        0.20 * regional
    )

    # 🔥 Stronger state influence
    base_score *= state_weight

    # 🔥 Monsoon effect as additive stress
    base_score += 0.1 * monsoon_factor

    base_score = max(0.05, min(base_score, 0.95))

    probability = 1 / (1 + math.exp(-2 * (base_score - 0.5)))

    confidence = abs(probability - 0.5) * 2

    return round(probability, 3), round(confidence, 3)