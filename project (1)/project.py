import requests
import folium
from folium.plugins import FloatImage
from folium.map import Layer
import re
import csv
import os
import datetime
from flask import Flask, render_template, request

# zorg ervoor dat het csv bestand leeg wordt geopend
csv_file_path = "cities.csv"

def clear_csv():
    with open(csv_file_path, "w", newline="") as file:
        file.truncate(0)
if os.path.exists(csv_file_path):
    clear_csv()


app = Flask(__name__)
# lege dictionary voor de search history
city_history = []
# set voor unieke steden namen
city_once = set()


# open csv bestand voor de search history
def history(csv_file_path="cities.csv"):
    with open(csv_file_path, "r", newline="") as file:
        reader = csv.reader(file)
        return [row[0] for row in reader if row]

# stop de search history in het net geopende csv bestand
def writehistory(city, csv_file_path="cities.csv"):
    with open(csv_file_path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([city])


# haal weerdata op
def fetch(location):
    api_url = "http://api.weatherstack.com/current"
    api_key = "98160d56c4f0ba69fe05dc9c8a659ef1"
    query = location

    response = requests.get(api_url, params={"access_key": api_key, "query": location})
    weather_data = response.json()

    return weather_data

# check of de input geen tekens bevat
def caracters(input_string):
    return bool(re.match("^[a-zA-Z ]+$", input_string))

@app.route("/clear_history")
def clear_history():
    clear_csv()
    city_once.clear()
    return main()

@app.route("/")
def main():
    location = request.args.get("city", "Amsterdam")

    # als input alleen normale karakters is wordt weerdata geprint anders de error message. Default stad wordt Amsterdam
    if not caracters(location):
        error_message = "Please enter a valid city"
        location = "Amsterdam"
        weather_data = fetch(location)
    else:
        weather_data = fetch(location)

        # als de gegeven input niet in de dictionary staat of gelijk is aan een variabale in "name" print dan de error code en geef de default stad weer
        if "location" not in weather_data or location.lower() != weather_data.get("location", {}).get("name", "").lower():
            error_message = "Please enter a valid city"
            location = "Amsterdam"
            weather_data = fetch(location)
        else:
            error_message = None

        # als de input locatie gelijk is aan amsterdam, print deze dan niet in de search history
        if location.lower() != "amsterdam":
            # zorg ervoor dat de steden maar 1x geprint worden in de search history
            if location.lower() not in city_once:
                writehistory(location)
                city_once.add(location.lower())

    # als de input locatie gelijk is aan amsterdam, print deze dan niet in de search history
    city_history = [city for city in history() if city.lower() != "amsterdam"]

    # verschillende weerdata ophalen uit het json bestand
    temperature = weather_data["current"]["temperature"]
    humidity = weather_data["current"]["humidity"]
    wind_speed = weather_data["current"]["wind_speed"]
    # verander de wind richting codes
    def change_winddir(wind_dir):
        winddirections = {
            "N": "North",
            "E": "East",
            "S": "South",
            "W": "West"
        }
        directions = []
        for char in wind_dir:
            new_direction = winddirections.get(char)
            if new_direction:
                directions.append(new_direction)
        return ", ".join(directions)

    winddir = weather_data["current"]["wind_dir"]
    new_wind = change_winddir(winddir)
    pressure = weather_data["current"]["pressure"]
    precipitation = weather_data["current"]["precip"]
    cloudcover = weather_data["current"]["cloudcover"]
    feelslike = weather_data["current"]["feelslike"]
    visibility = weather_data["current"]["visibility"]
    weer = weather_data["current"]["weather_descriptions"]
    weatherdes = ", ".join(weer)
    uv = weather_data["current"]["uv_index"]
    # haal de observatie tijd op en verander die in de 24 uurs klok en in de west europeese tijd
    time = weather_data["current"]["observation_time"]
    time_change = time.split()
    time_new = time_change[0].split(":")
    hours = int(time_new[0])
    minutes = int(time_new[1])
    if time_change[1] == "PM" and hours != 12:
        hours += 12
    hours += 1
    if hours >= 24:
        hours -= 24
    time_24 = f"{hours:02d}:{minutes:02d}"
    lat = float(weather_data["location"]["lat"])
    lon = float(weather_data["location"]["lon"])
    # haal lokale tijd van de gekoze stad op en geef allen de tijd niet de datum weer
    local_time_str = weather_data["location"]["localtime"]
    local_time_change = datetime.datetime.strptime(local_time_str, "%Y-%m-%d %H:%M")
    local_time_city_after = local_time_change.strftime("%H:%M")

    local_time_parts = local_time_city_after.split(":")
    local_hours = int(local_time_parts[0])
    local_minutes = int(local_time_parts[1])

    is_night = (local_hours >= 22 or local_hours <6)


    # geef kaart weer, locatie is gebasseerd op de opgevraagde locatie
    m = folium.Map(location=[lat, lon], zoom_start=11)
    folium.Marker([lat, lon], tooltip=location).add_to(m)

    if is_night:
        folium.TileLayer("cartodbdark_matter").add_to(m)
    else:
        # google maps traffic layer aan de kaart toevoegen
        traffic_layer = folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=m@221097413,traffic&hl=en&gl=US&src=app&x={x}&y={y}&z={z}&s=Galile",
            attr="Google Traffic",
            name="Traffic",
            overlay=True,
        )
        traffic_layer.add_to(m)


        # lagen aan en uit kunnen zetten
        folium.LayerControl().add_to(m)


    # geneer de kaart en geneer het html bestand met variabelen
    map_html = m.get_root().render()
    return render_template("map.html",
                           map_html=map_html,
                           temperature=temperature,
                           humidity=humidity,
                           wind_speed=wind_speed,
                           new_wind=new_wind,
                           winddir=winddir,
                           pressure=pressure,
                           precipitation=precipitation,
                           cloudcover=cloudcover,
                           feelslike=feelslike,
                           uv=uv,
                           visibility=visibility,
                           weatherdes=weatherdes,
                           time_24=time_24,
                           current_city=location,
                           error_message=error_message,
                           city_history=city_history,
                           local_time_city_after=local_time_city_after
                           )

if __name__ == "__main__":
    app.run(debug=True)
