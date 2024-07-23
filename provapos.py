import geocoder
from geopy.geocoders import Nominatim


def get_current_gps_coordinates():
    g = geocoder.ip('me')
    if g.latlng is not None: 
        return g.latlng
    else:
        return None




if __name__ == "__main__":
    coordinates = get_current_gps_coordinates()

    if coordinates is not None:
        latitude, longitude = coordinates
        print(f"Your current GPS coordinates are:")
        print(f"Latitude: {latitude}")
        print(f"Longitude: {longitude}")

        # calling the nominatim tool
        geoLoc = Nominatim(user_agent="GetLoc")
    

        pos = str(latitude) + ", " + str(longitude)
        # passing the coordinates
        locname = geoLoc.reverse(pos)

        print(locname)

    else:
        print("Unable to retrieve your GPS coordinates.")