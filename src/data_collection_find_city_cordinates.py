import requests

# La brukeren skrive inn en by
city = input("Skriv inn en by: ")

# Hent koordinater fra Open-Meteo Geocoding API
geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
geo_response = requests.get(geo_url)
geo_data = geo_response.json()

# Sjekk om vi fikk et resultat
if "results" in geo_data and geo_data["results"]:
    lat = geo_data["results"][0]["latitude"]
    lon = geo_data["results"][0]["longitude"]
    print(f"Koordinater for {city}: {lat}, {lon}")

    # Hent værdata for dette stedet
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=temperature_2m_max&timezone=Europe/Oslo"
    weather_response = requests.get(weather_url)
    weather_data = weather_response.json()

    print(f"Maks temperatur for {city}: {weather_data['daily']['temperature_2m_max']} °C")

else:
    print(f"Fant ikke koordinater for {city}.")

