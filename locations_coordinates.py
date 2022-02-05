""" Works with coordinates with the use of geopy module """

from functools import cache
from math import sin, cos, asin, radians
from math import sqrt

from geopy.geocoders import Nominatim
from geopy.distance import distance


class LocationsCoordinates:
    """ Gets location coordinates, distance between coordinates with the use of geopy module"""

    def __init__(self):
        self.geolocator = Nominatim(user_agent="Locations coordinates program")

    @staticmethod
    def haversine_formula(longitude_a: float, latitude_a: float,
                          longitude_b: float, latitude_b: float) -> float:
        """ Calculation of distance between two coordinates (haversine formula)

        >>> LocationsCoordinates.haversine_formula(-11.178288, 44.178288, -13.6082941, 66.3333333)
        2467.898441799789
        """
        r_longitude_a, r_latitude_a = radians(longitude_a), radians(latitude_a)
        r_longitude_b, r_latitude_b = radians(longitude_b), radians(latitude_b)

        delta_r_longitude = r_longitude_b - r_longitude_a
        delta_r_latitude = r_latitude_b - r_latitude_a

        part_1 = (sin(delta_r_latitude / 2) ** 2 +
                  cos(r_latitude_a) * cos(r_latitude_b) * sin(delta_r_longitude / 2) ** 2)
        part_2 = 2 * asin(sqrt(part_1))
        earth_radius = 6371
        calculated_distance = part_2 * earth_radius

        return calculated_distance

    @classmethod
    @cache
    def geopy_distance(cls, longitude_a: float, latitude_a: float,
                       longitude_b: float, latitude_b: float) -> float:
        """ Calculation of distance between two coordinates (geopy module), more accurate

        >>> LocationsCoordinates().geopy_distance(-11.178288, 44.178288, -13.6082941, 66.3333333)
        2423.2380620381737
        """

        return distance(
            (longitude_a, latitude_a),
            (longitude_b, latitude_b)
        ).km

    @cache
    def get_place_location(self, place_name: str) -> tuple:
        """ Get place location by it's name

        >>> LocationsCoordinates().get_place_location('Mountain View, CA')
        (37.3893889, -122.0832101)
        """

        try:
            location = self.geolocator.geocode(place_name)
            latitude, longitude = location.latitude, location.longitude
        except Exception:  # pylint: disable=broad-except
            latitude, longitude = None, None

        return latitude, longitude

    @cache
    def get_place_location_approx(self, place_name: str) -> tuple:
        """ Get approximate place location by it's name.
        Works by trying to get place location with the use of get_place_location
        by place levels

        MyHouse, Mountain View, CA -> Mountain View, CA
        Not found                  -> Found

        >>> LocationsCoordinates().get_place_location_approx('MyHouse, Mountain View, CA')
        (37.3893889, -122.0832101)
        """
        place_name_split = place_name.split(', ')

        for place_level in range(len(place_name_split)):
            latitude, longitude = self.get_place_location(', '.join(place_name_split[place_level:]))

            if latitude and longitude:
                return float(latitude), float(longitude)
        return None, None


if __name__ == '__main__':
    locations = LocationsCoordinates()
    for i in range(100):
        print(locations.get_place_location_approx('TestLocation, Mountain View, CA'))
