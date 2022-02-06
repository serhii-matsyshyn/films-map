""" Works with map with the use of folium method """

import os
from logging import info

import pandas as pd
import folium


class LocationsMap:
    """ Creates map with films based on provided data """

    def __init__(self, center_latitude: float, center_longitude: float,
                 year: int, save_to: str = 'map.html'):
        self.center_latitude, self.center_longitude = center_latitude, center_longitude
        self.year = year
        self.save_to = save_to

        self.map = folium.Map(location=[self.center_latitude, self.center_longitude],
                              zoom_start=3)
        self.map.add_child(folium.Marker(location=[center_latitude, center_longitude],
                                         popup="Center location",
                                         icon=folium.Icon(color='red', icon='user', prefix='fa'))
                           )

    def save_map(self):
        """ Save map to html file"""
        # create map directory if not exists
        if ((len(os.path.dirname(self.save_to)) > 1) and
                (not os.path.exists(os.path.dirname(self.save_to)))):
            os.makedirs(os.path.dirname(self.save_to))
        self.map.save(self.save_to)

        info(f"Saved map to {self.save_to}")

    def create_map(self, df_films: pd.DataFrame):
        """ Create map based on provided pd.DataFrame """
        fg_film_markers = folium.FeatureGroup(name=f"Nearest films in {self.year}")
        fg_path = folium.FeatureGroup(name="Shortest path to film location")

        for _, film in df_films.iterrows():
            film_latitude, film_longitude = film['latitude'], film['longitude']
            fg_film_markers.add_child(
                folium.Marker(location=[film_latitude, film_longitude],
                              popup=f"Film: {film['name']}",
                              icon=folium.Icon(icon="video-camera", prefix='fa'))
            )

            fg_path.add_child(
                folium.PolyLine([[film_latitude, film_longitude],
                                 [self.center_latitude, self.center_longitude]],
                                color="red", weight=2.5, opacity=1,
                                popup=f"Distance: {film['distance']}")
            )

        self.map.add_child(fg_film_markers)
        self.map.add_child(fg_path)
        self.map.add_child(folium.LayerControl())

        info("Created map")

        self.save_map()
