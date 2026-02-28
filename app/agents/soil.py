def nitrogen_factor(days_since_nitrogen: int) -> float:
    """
    Returns vulnerability factor based on recent nitrogen application.
    High nitrogen makes crop more susceptible to blast.
    """

    if days_since_nitrogen < 10:
        return 0.9
    elif days_since_nitrogen < 20:
        return 0.6
    else:
        return 0.3