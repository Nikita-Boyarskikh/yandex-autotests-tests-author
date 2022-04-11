import pytest

from shipping import get_price, Fragility, UnableToDeliver, Size, Load, MIN_PRICE


class TestGetPrice:
    def test_min_price(self):
        assert get_price(0) == MIN_PRICE

    def test_unable_to_deliver_fragile_shipping_to_30km(self):
        with pytest.raises(UnableToDeliver):
            get_price(30.001, fragility=Fragility.FRAGILE)

    def test_unable_to_deliver_fragile_shipping_to_longer_distance(self):
        with pytest.raises(UnableToDeliver):
            get_price(12345, fragility=Fragility.FRAGILE)

    @pytest.mark.parametrize(
        ('distance', 'expected'),
        (
            # price for large shipping with extra high load = (distance margin + 200) * 1.6
            (0.999, 400),
            (1.999, 400),
            (2.000, 480),
            (9.999, 480),
            (10.00, 640),
            (29.99, 640),
            (30.00, 800),
            (999.9, 800),
        ),
    )
    def test_distance(self, distance, expected):
        assert get_price(distance, size=Size.LARGE, load=Load.EXTRA_HIGH) == expected

    @pytest.mark.parametrize(
        ('size', 'expected'),
        (
            (Size.SMALL, 400),
            (Size.LARGE, 500),
        )
    )
    def test_size(self, size, expected):
        assert get_price(30, size=size) == expected

    @pytest.mark.parametrize(
        ('fragility', 'expected'),
        (
            (Fragility.NORMAL, 400),
            (Fragility.FRAGILE, 700),
        )
    )
    def test_fragility(self, fragility, expected):
        assert get_price(30, fragility=fragility) == expected

    @pytest.mark.parametrize(
        ('load', 'expected'),
        (
            (Load.USUAL, 400),
            (Load.ABOVE_USUAL, 480),
            (Load.HIGH, 560),
            (Load.EXTRA_HIGH, 640),
        )
    )
    def test_load(self, load, expected):
        assert get_price(30, load=load) == expected
