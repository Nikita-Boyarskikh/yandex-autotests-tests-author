import enum


class UnableToDeliver(ValueError):
    pass


class Load(enum.Enum):
    EXTRA_HIGH = 'extra-high'
    HIGH = 'high'
    ABOVE_USUAL = 'above-usual'
    USUAL = 'usual'

    def __str__(self):
        return self.value


class Size(enum.Enum):
    LARGE = 'large'
    SMALL = 'small'

    def __str__(self):
        return self.value


class Fragility(enum.Enum):
    FRAGILE = 'fragile'
    NORMAL = 'normal'

    def __str__(self):
        return self.value


MIN_PRICE: float = 400

FRAGILITY_MARGIN_MAP = {
    Fragility.FRAGILE: 300,
    Fragility.NORMAL: 0,
}

SIZE_MARGIN_MAP = {
    Size.SMALL: 100,
    Size.LARGE: 200,
}

LOAD_MULTIPLIER_MAP = {
    Load.USUAL: 1,
    Load.ABOVE_USUAL: 1.2,
    Load.HIGH: 1.4,
    Load.EXTRA_HIGH: 1.6,
}

DISTANCE_MARGIN_TO_MAP = {
    2: 50,
    10: 100,
    30: 200,
    float('inf'): 300,
}


def _get_distance_margin(distance: float) -> float:
    for max_distance, margin in DISTANCE_MARGIN_TO_MAP.items():
        if distance < max_distance:
            return margin


def get_price(
        distance: float,
        size: Size = Size.SMALL,
        fragility: Fragility = Fragility.NORMAL,
        load: Load = Load.USUAL,
) -> float:
    if fragility == Fragility.FRAGILE and distance > 30:
        raise UnableToDeliver()

    price = _get_distance_margin(distance) + SIZE_MARGIN_MAP[size] + FRAGILITY_MARGIN_MAP[fragility]
    load_multiplier = LOAD_MULTIPLIER_MAP[load]

    total_price = price * load_multiplier
    return max(MIN_PRICE, total_price)
