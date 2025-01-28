import streamlit as st
from opencage.geocoder import OpenCageGeocode
from geopy.distance import geodesic
import requests

# Initialize OpenCage geocoder
opencage_key = 'd7a6a9980e1244649ea85b91d50d555a'  # Replace with your OpenCage API key
geocoder = OpenCageGeocode(opencage_key)

# Function to find the nearest hospitals
def find_nearest_hospitals_osm(pin_code):
    # Geocode the pin code
    results = geocoder.geocode(pin_code)
    if not results:
        return None

    lat, lng = results[0]['geometry']['lat'], results[0]['geometry']['lng']
    user_location = (lat, lng)

    # Use Overpass API to find nearby hospitals within a radius
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    node["amenity"="hospital"](around:10000,{lat},{lng});
    out;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})

    if response.status_code != 200:
        return None

    data = response.json()
    if not data['elements']:
        return None

    # Find the nearest hospitals
    hospitals = []
    for hospital in data['elements']:
        hospital_location = (hospital['lat'], hospital['lon'])
        distance = geodesic(user_location, hospital_location).meters
        hospital_name = hospital.get('tags', {}).get('name', 'Unnamed Hospital')
        hospitals.append((hospital_name, hospital_location, distance))

    # Sort hospitals by distance and get the two nearest
    hospitals.sort(key=lambda x: x[2])
    nearest_hospitals = hospitals[:2]  # Get the two nearest hospitals

    hospital_info_list = []
    for hospital in nearest_hospitals:
        name, location, distance = hospital
        hospital_lat, hospital_lon = location

        # Reverse geocode for detailed address
        reverse_results = geocoder.reverse_geocode(hospital_lat, hospital_lon)
        detailed_address = reverse_results[0]['formatted'] if reverse_results else "Address not available"

        hospital_info_list.append({
            "name": name,
            "address": detailed_address,
            "distance": f"{distance:.2f} meters"
        })

    return hospital_info_list

# Streamlit interface
st.title("MEDAI - Nearest Hospital Finder")

# Input for pin code
pin_code = st.text_input("Enter your pin code to find hospitals near you:")

# Find button
if st.button("Find Nearest Hospitals"):
    # Find hospital information based on pin code
    hospital_info_list = find_nearest_hospitals_osm(pin_code)
    if hospital_info_list:
        st.subheader("Nearest Hospitals:")
        for hospital_info in hospital_info_list:
            st.write(f"**Name:** {hospital_info['name']}")
            st.write(f"**Address:** {hospital_info['address']}")
            st.write(f"**Distance:** {hospital_info['distance']}")
            st.write("---")  # Separator between hospitals
    else:
        st.error("No hospitals found or invalid pin code.")


