from app.fusion.epidemic import simulate_spread, apply_intervention, climate_scenario_adjustment
from app.agents.weather import get_weather_forecast
from app.agents.soil import nitrogen_factor
from app.agents.regional import regional_risk
from app.agents.yield_model import estimate_yield_loss
from app.agents.calibration import (
    state_weight,
    monsoon_boost,
    historical_normalization
)
from app.fusion.engine import compute_risk


def growth_sensitivity(days_after_sowing: int) -> float:
    if 15 <= days_after_sowing <= 45:
        return 1.0
    elif 46 <= days_after_sowing <= 70:
        return 0.6
    else:
        return 0.3


def run_prediction(lat, lon, nitrogen_days, sowing_days, state):

    weather = get_weather_forecast(lat, lon)
    nitrogen = nitrogen_factor(nitrogen_days)
    regional = regional_risk(lat, lon)
    growth = growth_sensitivity(sowing_days)

    s_weight = state_weight(state)
    monsoon = monsoon_boost()

    probability, confidence = compute_risk(
        weather,
        nitrogen,
        regional,
        growth,
        s_weight,
        monsoon
    )

    normalized_prob = historical_normalization(probability)

    # Prevent saturation before simulation
    adjusted_prob = min(normalized_prob * 0.9, 0.85)

    adjusted_prob = climate_scenario_adjustment(
        adjusted_prob,
        scenario="normal"
    )

    spread_curve = simulate_spread(adjusted_prob, days=7)

    intervention_curve = apply_intervention(
        spread_curve,
        fungicide=True,
        reduce_nitrogen=True
    )

    yield_loss = estimate_yield_loss(
        adjusted_prob,
        sowing_days,
        nitrogen,
        regional,
        growth
    )

    return {
        "blast_probability": adjusted_prob,
        "confidence_score": confidence,
        "projected_yield_loss_percent": yield_loss,
        "spread_forecast": spread_curve,
        "intervention_forecast": intervention_curve,
        "details": {
            "weather_indices": weather,
            "nitrogen_factor": nitrogen,
            "regional_risk": regional,
            "growth_factor": growth,
            "state_weight": s_weight,
            "monsoon_factor": monsoon
        }
    }