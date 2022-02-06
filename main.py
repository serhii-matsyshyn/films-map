""" Main module used to create map with the 10 nearest films locations in certain year
by provided console input
"""

import argparse
from typing import Callable

from films_locations import FilmsLocations

# pylint: disable = import-error  # To disable import-error warning


def parse_args() -> argparse.Namespace:
    """ Parses args using argparse
    python main.py 2016 49.83826 24.02324 "datasets/locations_100.list" --save_map_to "map.html"
    """
    parser = argparse.ArgumentParser(
        description='''Films map module, creates html page.
        The web map shows information about the locations
        of the 10 nearest filming locations of films that were shot in a given year.
        Location information is taken from imdb locations list.'''
    )
    parser.add_argument(
        'year',
        type=int,
        help='''Year of films to search for'''
    )
    parser.add_argument(
        'latitude',
        type=float,
        help='''Latitude of center location (your own location)'''
    )
    parser.add_argument(
        'longitude',
        type=float,
        help='''Longitude of center location (your own location)'''
    )
    parser.add_argument(
        'path_to_dataset',
        type=str,
        help='''Path to dataset'''
    )
    parser.add_argument(
        '--save_map_to',
        type=str,
        default='map.html',
        help='''Save html map to'''
    )
    return parser.parse_args()


def exception_handler(function: Callable,
                      args: argparse.Namespace):
    """ Function to catch unexpected exceptions """
    try:
        function(args)
    except ValueError:
        print("Error!")
        print("You provided corrupted locations list \
or none correct films in provided year were found.")
    except (Exception,) as err:  # pylint: disable=broad-except
        # Catches all errors that were not caught by previous checks.
        print("Error: Unexpected exception occured.")
        print(f"Detailed error: {err}")


def make_films_map(args: argparse.Namespace):
    """ Make films map by provided argparse.Namespace """
    locations = FilmsLocations(args.year, args.latitude, args.longitude,
                               dataset_filename=args.path_to_dataset)
    locations.process()


def main():
    """ Main function of the program """
    args = parse_args()
    exception_handler(make_films_map, args)


if __name__ == '__main__':
    main()
