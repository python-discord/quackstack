def clamp(min_val: float, max_val: float, value: float):
    return sorted((min_val, value, max_val))[1]
