""" Works with dataset of films locations, parses dataset and uses it to create map """

# pylint: disable = invalid-name  # To disable "df" variable warning
# pylint: disable = import-error,too-many-arguments,no-member

from logging import debug, info

import pandas as pd

from locations_coordinates import LocationsCoordinates
from locations_map import LocationsMap


pd.options.mode.chained_assignment = None
# pd.set_option('display.max_rows', 2000000)
pd.set_option('display.max_columns', 5000)
pd.set_option('display.width', 1000)


class FilmsLocations:
    """ Parses and normalizes films locations list,
    uses this data to calculate the 10 nearest filming locations,
    and creates map with these locations
    """

    def __init__(self, films_year,
                 center_latitude, center_longitude,
                 dataset_filename="locations_100.list",
                 save_to: str = 'map.html'):
        self.films_year = films_year
        self.center_longitude = center_longitude
        self.center_latitude = center_latitude

        self.locations_coordinates = LocationsCoordinates()
        self.locations_map = LocationsMap(center_latitude, center_longitude, films_year,
                                          save_to=save_to)
        self.df = pd.read_csv(
            dataset_filename,
            encoding='ansi',
            skiprows=14,  # skip 14 heading rows
            index_col=False,  # new index column
            names=["empty", "name", "year", "info1", "location", "info2"],  # read data of locations
            on_bad_lines='skip',  # drop "bad lines"
            # custom regex to parse data
            sep=r"^(.*)(?: )(\([^TV]*\))(?: |\t*?)(\{.*\}|\(.*\))*(?:\t+)([^\t\n]*)(?:\t)*(\(.*)?$",
            engine='python'
        )

        self.df = self.df.drop(labels="empty", axis=1)  # drop empty column
        self.df = self.df.drop_duplicates(subset=["name", "year", "location"])
        # parse year, convert year to int64
        self.df.year = self.df.year.apply(
            lambda year: int(year[1:5]) if year and ('?' not in year) else -1
        )

        debug("Parsed dataset:")
        debug(self.df)

    def create_locations_coordinates(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Creates coordinates from locations names
        and adds them as columns latitude, longitude to df
        """
        df[['latitude', 'longitude']] = df.apply(
            lambda rows: pd.Series(
                self.locations_coordinates.get_place_location_approx(rows['location'])
            ),
            axis=1)
        df = df.dropna(subset=['latitude', 'longitude'])  # remove locations that were not found

        return df

    def create_distance_to_center(self, df: pd.DataFrame) -> pd.DataFrame:
        """ Creates column with the distance
        from center location to film location coordinates
        """
        df['distance'] = df.apply(
            lambda rows: self.locations_coordinates.geopy_distance(
                self.center_latitude,
                self.center_longitude,
                rows['latitude'],
                rows['longitude']
            ),
            axis=1)
        return df

    def process(self):
        """ Process the provided data to create map """
        # select films with certain year
        info('Starting FilmsLocations main process')

        selected_df = self.df[self.df['year'] == self.films_year]
        info(f"Selected films with {self.films_year} year")
        debug(selected_df)

        # create coordinates from locations
        info("Starting getting coordinates from locations name, can take some time...")
        selected_df = self.create_locations_coordinates(selected_df)
        info("Created coordinates from locations")
        debug(selected_df)

        # create distance to central coordinates
        selected_df = self.create_distance_to_center(selected_df)
        info("Created distance to central coordinates")
        debug(selected_df)

        # get up to 10 locations nearest to center location
        final_nearest_df = selected_df.nsmallest(10, 'distance')
        info("Got up to 10 locations nearest to center location")
        debug(final_nearest_df)

        self.locations_map.create_map(final_nearest_df)


if __name__ == '__main__':
    own_latitude, own_longitude = 49.83826, 24.02324
    locations = FilmsLocations(2015, own_latitude, own_longitude,
                               dataset_filename="datasets/locations_100.list")
    locations.process()
