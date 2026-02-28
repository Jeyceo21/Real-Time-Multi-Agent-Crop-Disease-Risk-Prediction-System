def simulate_spread(initial_risk, days=7):

    risks = [round(initial_risk, 3)]

    for _ in range(days):
        growth_rate = 0.18

        next_risk = risks[-1] + growth_rate * risks[-1] * (1 - risks[-1])

        # Never allow perfect saturation
        next_risk = min(next_risk, 0.92)

        risks.append(round(next_risk, 3))

    return risks


def apply_intervention(risk_curve, fungicide=True, reduce_nitrogen=True):

    modified = []

    for r in risk_curve:
        reduction_factor = 1.0

        if fungicide:
            reduction_factor *= 0.75
        if reduce_nitrogen:
            reduction_factor *= 0.85

        new_risk = r * reduction_factor
        modified.append(round(new_risk, 3))

    return modified


def climate_scenario_adjustment(risk, scenario="normal"):

    if scenario == "excess_rain":
        return min(risk * 1.1, 0.95)
    elif scenario == "drought":
        return risk * 0.85
    else:
        return risk