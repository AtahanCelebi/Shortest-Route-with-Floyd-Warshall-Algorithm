import folium
import pandas as pd
def main(path_v2):
    def create_map(name,lat_list,long_list):
       int_lat = [float(i) for i in lat_list ]
       int_long = [float(i) for i in long_list]

       # Make a data frame with dots to show on the map
       data = pd.DataFrame({
           'lat': int_long ,
           'lon': int_lat,
           'name': name
       })
       data
       # Make an empty map
       m = folium.Map(location=[20, 0], tiles="Mapbox Bright", zoom_start=2)

       # I can add marker one by one on the map
       for i in range(0, len(data)):
           folium.Marker([data.iloc[i]['lon'], data.iloc[i]['lat']], popup=data.iloc[i]['name']).add_to(m)

       # Save it as html
       m.save('unknown.html')


    data = path_v2
    #f = open(path_v2,"r")

    #lines = list(f)
    #data = []
    #for i in lines:
     #   data.append(i.split(","))
    #for i in range(len(data)):
     #   data[i][0] = str(i +1)



    lati = list()
    longi = list()
    airport_name = list()
    airport_data = list()
    for i in range(len(data)):
        lati.append(data[i][6])
        longi.append(data[i][7])
        airport_name.append(data[i][1])
        airport_data.append(data[i][0])
    create_map(airport_name,lati,longi)



    from geopy.geocoders import Nominatim
    from geopy.distance import great_circle

    geolacator = Nominatim(user_agent="Hacettepe_Geomatik")

    edges = []

    for j in range(len(data)):

        loc_choosen = airport_data[j]
        v = [data[j][6],data[j][7]]
        airport_choosen = (float(data[j][6]), float(data[j][7]))

        for i in range(len(lati)):

            location2 = airport_data[i]
            airport2 = (float(data[i][6]), float(data[i][7]))
            if loc_choosen == location2:
                edges.append([int(loc_choosen),int(location2),99999])
            edges.append([int(loc_choosen),int(location2),great_circle(airport_choosen, airport2).km])
    return edges,len(airport_data)
