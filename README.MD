# Films map

Creates an html map with up to the 10 nearest films locations in a certain year by provided console input.  
The web map shows information about the locations of films that were shot in a given year and the distance to them.

## Information provided by the map
The module allows you to get information about the nearest filming locations in the form of a web map.  
This allows you to visualize a list of movie data and find out where the nearest movie locations are.  
Sorting by film recording date allows you to select locations that were shot in a particular year.  
You can also find out the distance to the location and the nearest route.  
There are 3 layers of the map - the main one, the layer with location labels and the layer with paths to locations (distance to location).  

## Installation

Install the requirements:

```bash
pip install -r requirements.txt
```

## Usage

Call the module from the command line for movies for which year you want to build a map and your location as latitude and longitude (eg 49.83826,24.02324) and optionally the location of the file where you want to save the map. The result is an HTML file.

```bash
python main.py 2016 49.83826 24.02324 "datasets/locations_100.list" --save_map_to "map.html"
```

## Example
![images/img.png](images/img.png)

![images/img2.png](images/img2.png)

![images/img3.png](images/img3.png)
