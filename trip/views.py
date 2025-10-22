from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TripInputSerializer
from .models import Trip
import traceback
import requests
import json
from math import radians, cos, sin, asin, sqrt

def get_coordinates(address):
    try:
        url = "https://nominatim.openstreetmap.org/search"
        params = {'q': address, 'format': 'json', 'limit': 1}
        headers = {'User-Agent': 'TripPlannerApp/1.0'}
        response = requests.get(url, params=params, headers=headers)
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
        else:
            return None, None
    except Exception as e:
        print(f"Error fetching coordinates for {address}: {e}")
        return None, None

def haversine(lat1, lon1, lat2, lon2):
    R = 3956
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

def generate_logs(total_miles, cycle_used, pickup_location, dropoff_location):
    logs = []
    remaining_hours = 70 - cycle_used
    day = 1
    miles_remaining = total_miles
    fuel_counter = 0
    notes = f"Departed {pickup_location}"

    while remaining_hours > 0 and miles_remaining > 0:
        driving = min(11, remaining_hours)
        rest = 10
        fuelStop = fuel_counter >= 1000

        logs.append({
            "day": f"Day {day}",
            "driving": driving,
            "rest": rest,
            "fuelStop": fuelStop,
            "notes": notes
        })

        remaining_hours -= driving
        miles_remaining -= driving * 60
        fuel_counter += driving * 60
        if fuelStop:
            fuel_counter = 0
            notes = "Refueled en route"
        elif miles_remaining <= 0:
            notes = f"Reached {dropoff_location}"
        else:
            notes = f"Driving day {day}"

        day += 1

    return logs

@api_view(['POST'])
def generate_trip(request):
    try:
        serializer = TripInputSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data

            current_lat, current_lng = get_coordinates(data['current_location'])
            pickup_lat, pickup_lng = get_coordinates(data['pickup_location'])
            dropoff_lat, dropoff_lng = get_coordinates(data['dropoff_location'])

            if None in [current_lat, current_lng, pickup_lat, pickup_lng, dropoff_lat, dropoff_lng]:
                return Response({ "error": "Unable to fetch coordinates for one or more locations." }, status=400)

            map_points = [
                { "lat": current_lat, "lng": current_lng, "label": f"📍 Current Location: {data['current_location']}" },
                { "lat": pickup_lat, "lng": pickup_lng, "label": f"📦 Pickup Location: {data['pickup_location']}" },
                { "lat": dropoff_lat, "lng": dropoff_lng, "label": f"🏁 Dropoff Location: {data['dropoff_location']}" },
            ]

            leg1 = haversine(current_lat, current_lng, pickup_lat, pickup_lng)
            leg2 = haversine(pickup_lat, pickup_lng, dropoff_lat, dropoff_lng)
            total_miles = leg1 + leg2

            logs = generate_logs(total_miles, data['cycle_used'], data['pickup_location'], data['dropoff_location'])

            trip = Trip.objects.create(
                current_location=data['current_location'],
                pickup_location=data['pickup_location'],
                dropoff_location=data['dropoff_location'],
                cycle_used=data['cycle_used'],
                total_miles=total_miles
            )
            trip.set_map_points(map_points)
            trip.set_logs(logs)
            trip.save()

            return Response({ "mapPoints": map_points, "logs": logs })

        return Response(serializer.errors, status=400)

    except Exception as e:
        print("Exception occurred:", str(e))
        traceback.print_exc()
        return Response({ "error": "Internal server error" }, status=500)
