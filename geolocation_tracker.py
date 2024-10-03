import requests
import folium

def get_ip():
    """Fetches the user's public IP address."""
    try:
        response = requests.get("https://api64.ipify.org?format=json")
        response.raise_for_status()
        return response.json()["ip"]
    except requests.RequestException as e:
        print(f"Error fetching IP address: {e}")
        return None

def get_geolocation(ip):
    """Fetches geolocation data from an IP address."""
    try:
        # API that provides geolocation data from an IP address
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        response.raise_for_status()
        data = response.json()
        return {
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country_name"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude")
        }
    except requests.RequestException as e:
        print(f"Error fetching geolocation: {e}")
        return None

def display_map(latitude, longitude, city, region, country):
    """Displays the location on a map using folium."""
    # Create a map centered at the given latitude and longitude
    location_map = folium.Map(location=[latitude, longitude], zoom_start=10)
    
    # Add a marker at the location
    folium.Marker([latitude, longitude], 
                  popup=f"Location: {city}, {region}, {country}",
                  tooltip="Click for more info").add_to(location_map)
    
    # Save the map to an HTML file
    location_map.save("geolocation_map.html")
    print("Map has been saved as 'geolocation_map.html'")

def main():
    print("Fetching your public IP address...")
    ip = get_ip()
    
    if ip:
        print(f"Your IP address is: {ip}")
        print("Fetching geolocation data...")
        geo_data = get_geolocation(ip)
        
        if geo_data:
            print(f"Location: {geo_data['city']}, {geo_data['region']}, {geo_data['country']}")
            print(f"Coordinates: {geo_data['latitude']}, {geo_data['longitude']}")
            
            # Display the location on the map
            display_map(geo_data['latitude'], geo_data['longitude'], 
                        geo_data['city'], geo_data['region'], geo_data['country'])
        else:
            print("Could not fetch geolocation data.")
    else:
        print("Could not fetch your IP address.")

if __name__ == "__main__":
    main()
