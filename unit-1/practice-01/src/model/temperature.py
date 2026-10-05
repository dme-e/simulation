def get_temperature_factor(temperature):
    if temperature <= 10:
        return 1.00
    elif temperature <= 12:
        return 0.90
    elif temperature <= 14:
        return 0.80
    elif temperature <= 16:
        return 0.70
    elif temperature <= 18:
        return 0.60
    elif temperature <= 20:
        return 0.50
    elif temperature <= 22:
        return 0.40
    elif temperature <= 24:
        return 0.30
    elif temperature <= 26:
        return 0.20
    else:
        return 0.10