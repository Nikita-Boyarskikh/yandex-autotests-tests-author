#!python
import argparse
import sys

from shipping import get_price, Size, Fragility, Load, UnableToDeliver


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description='Calculate shipping price in rubles')
    parser.add_argument('-d', '--distance', type=float, required=True, help='Shipping distance (km)')
    parser.add_argument('-l', '--large', action='store_true', default=False, help='Is shipment large')
    parser.add_argument('-f', '--fragile', action='store_true', default=False, help='Is shipment fragile')
    parser.add_argument('-o', '--load', type=Load, choices=list(Load), default=Load.USUAL, help='Shipment service load')

    return parser.parse_args(argv or sys.argv[1:])


if __name__ == '__main__':
    args = parse_args()

    try:
        price = get_price(
            distance=args.distance,
            size=Size.LARGE if args.large else Size.SMALL,
            fragility=Fragility.FRAGILE if args.fragile else Fragility.NORMAL,
            load=args.load,
        )
        print(price)
    except UnableToDeliver:
        print('Unable to deliver fragile shipping further than 30 km')
        exit(2)
