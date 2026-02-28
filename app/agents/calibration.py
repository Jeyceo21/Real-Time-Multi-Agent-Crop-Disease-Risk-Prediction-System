import random


# 🔹 State-Specific Risk Weight
def state_weight(state):

    weights = {
        "TamilNadu": 0.9,
        "Punjab": 0.75,
        "UttarPradesh": 1.1,
        "AndhraPradesh": 1.0,
        "Chhattisgarh": 1.15,
        "WestBengal": 1.2
    }

    return weights.get(state, 1.0)


# 🔹 Monsoon Boost (Seasonal Effect)
def monsoon_boost():

    # Slight variability for realism
    return round(random.uniform(0.9, 1.1), 2)


# 🔹 Historical Normalization (Prevents Extreme Saturation)
def historical_normalization(probability):

    # Keep risk in realistic biological range
    probability = max(0.05, min(probability, 0.9))

    # Mild historical smoothing
    normalized = 0.85 * probability + 0.15 * 0.5

    return round(normalized, 3)