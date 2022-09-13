import folium
import wget
import pandas as pd

# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon


spacex_csv_file = wget.download('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_geo.csv')
spacex_df=pd.read_csv(spacex_csv_file)


# Select relevant sub-columns: `Launch Site`, `Lat(Latitude)`, `Long(Longitude)`, `class`
spacex_df = spacex_df[['Launch Site', 'Lat', 'Long', 'class']]
launch_sites_df = spacex_df.groupby(['Launch Site'], as_index=False).first()
launch_sites_df = launch_sites_df[['Launch Site', 'Lat', 'Long']]


# Start location is NASA Johnson Space Center
nasa_coordinate = [29.559684888503615, -95.0830971930759]
site_map = folium.Map(location=nasa_coordinate, zoom_start=10)

# Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
circle = folium.Circle(nasa_coordinate, radius=1000, color='#d35400', fill=True).add_child(folium.Popup('NASA Johnson Space Center'))
# Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
marker = folium.map.Marker(
    nasa_coordinate,
    # Create an icon as a text label
    icon=DivIcon(
        icon_size=(20,20),
        icon_anchor=(0,0),
        html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % 'NASA JSC',
        )
    )
site_map.add_child(circle)
site_map.add_child(marker)

# Initial the map
site_map = folium.Map(location=nasa_coordinate, zoom_start=5)

# For each launch site, add a Circle object based on its coordinate (Lat, Long) values. In addition, add Launch site name as a popup label
for lat, lng, site in zip(spacex_df['Lat'], spacex_df['Long'], spacex_df['Launch Site']):
    # Create a blue circle at NASA Johnson Space Center's coordinate with a popup label showing its name
    #circle = folium.Circle([lat, lng], radius=1000, color='#d35400', fill=True).add_child(folium.Popup(site))
    # Create a blue circle at NASA Johnson Space Center's coordinate with a icon showing its name
    marker = folium.map.Marker(
        [lat, lng],
        # Create an icon as a text label
        icon=DivIcon(
            icon_size=(20,20),
            icon_anchor=(0,0),
            html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % site,
            )
        )
    site_map.add_child(circle)
    site_map.add_child(marker)
    
    
    # Function to assign color to launch outcome
def assign_marker_color(launch_outcome):
    if launch_outcome == 1:
        return 'green'
    else:
        return 'red'
    
spacex_df['marker_color'] = spacex_df['class'].apply(assign_marker_color)


# Add marker_cluster to current site_map

# for each row in spacex_df data frame
# create a Marker object with its coordinate
# and customize the Marker's icon property to indicate if this launch was successed or failed, 
# e.g., icon=folium.Icon(color='white', icon_color=row['marker_color']
site_map.add_child(marker_cluster)

for index, record in spacex_df.iterrows():
    marker = folium.Marker([record['Lat'], record['Long']], 
                  icon=folium.Icon(color='white', icon_color=record['marker_color']))
    marker_cluster.add_child(marker)
    
# Add Mouse Position to get the coordinate (Lat, Long) for a mouse over on the map
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
mouse_position = MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=False,
    num_digits=20,
    prefix='Lat:',
    lat_formatter=formatter,
    lng_formatter=formatter,
)

site_map.add_child(mouse_position)


from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance
  
# find coordinate of the closet coastline
coastline_lat = 28.56738
coastline_lon = -80.56885
launch_site_lat = 28.56341
launch_site_lon = -80.5768
distance_coastline = calculate_distance(launch_site_lat, launch_site_lon, coastline_lat, coastline_lon)

# Create and add a folium.Marker on your selected closest coastline point on the map
# Display the distance between coastline point and launch site using the icon property 
# for example

distance_marker = folium.Marker(
    [coastline_lat, coastline_lon],
    icon=folium.DivIcon(icon_size=(20,20),
                     icon_anchor=(0,0),
    html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_coastline),)
  )
site_map.add_child(distance_marker)

lines=folium.PolyLine(locations=[[launch_site_lat, launch_site_lon],[coastline_lat, coastline_lon]], weight=1)
site_map.add_child(lines)

# Create a marker with distance to a closest city, railway, highway, etc.
# Draw a line between the marker to the launch site
distance_city = calculate_distance(coastline_lat, coastline_lon, 28.60752, -80.81125)

distance_marker = folium.Marker(
    [28.60752, -80.81125],
    icon=folium.DivIcon(icon_size=(20,20),
                     icon_anchor=(0,0),
    html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_city),)
  )
site_map.add_child(distance_marker)

city=folium.PolyLine(locations=[[launch_site_lat, launch_site_lon],[28.60752, -80.81125]], weight=1)
site_map.add_child(city)

distance_railway = calculate_distance(coastline_lat, coastline_lon, 28.57171, -80.58513)

distance_marker = folium.Marker(
    [28.57171, -80.58513],
    icon=folium.DivIcon(icon_size=(20,20),
                     icon_anchor=(0,0),
    html='<div style="font-size: 12; color:#d35400;"><b>%s</b></div>' % "{:10.2f} KM".format(distance_railway),)
  )
site_map.add_child(distance_marker)

railway = folium.PolyLine(locations=[[launch_site_lat, launch_site_lon],[28.57171, -80.58513]], weight=1)
site_map.add_child(railway)

