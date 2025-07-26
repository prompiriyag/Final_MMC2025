from pyproj import Transformer
from shapely.geometry import Polygon
from geopy.distance import geodesic

latlon_coords = [
    (18 + 27/60 + 19/3600, 100 + 50/60 + 9/3600),   
    (18 + 27/60 + 19/3600, 100 + 51/60 + 37/3600), 
    (18 + 26/60 + 18/3600, 100 + 51/60 + 37/3600),  
    (18 + 26/60 + 18/3600, 100 + 50/60 + 9/3600),   
]
transformer = Transformer.from_crs("EPSG:4326", "EPSG:32647", always_xy=True)
projected_coords = [transformer.transform(lon, lat) for lat, lon in latlon_coords]
projected_coords.append(projected_coords[0])
polygon = Polygon(projected_coords)
area_m2 = polygon.area
area_rai = area_m2 / 1600
area_km2 = area_m2 / 1_000_000
print(area_m2,", ",area_rai,", ",area_km2)