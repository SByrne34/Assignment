from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile 
from django.contrib.gis.geos import Point
from .models import Pitch
from world.serializers import PitchSerializer
from rest_framework import generics
from geopy.geocoders import Nominatim
from rest_framework import generics

def homepage(request):
    return render(request, 'homepage.html')  # Renders the "homepage.html" template

# View that reads the locations from world borders and passes them to the map
@login_required
def map_view(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
        location = user_profile.location
    except Profile.DoesNotExist:
        location = None

    return render(request, 'map.html', {'user': request.user, 'location': location})

def update_location(request):   
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        user = request.profile
        user.location = Point(float(longitude), float(latitude))
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('homepage')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

geolocator = Nominatim(user_agent="location")

class ListCreateGenericViews(generics.ListCreateAPIView):
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer
 
    def perform_create(self, serializer):
        address = serializer.initial_data["address"]
        g = geolocator.geocode(address)
        lat = g.latitude
        lng = g.longitude
        pnt = Point(lng, lat)
        print(pnt)
        serializer.save(location=pnt)

class PitchUpdateRetreiveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pitch.objects.all()
    serializer_class = PitchSerializer
 
    def perform_update(self, serializer):
        address = serializer.initial_data["address"]
        g = geolocator.geocode(address)
        lat = g.latitude
        lng = g.longitude
        pnt = Point(lng, lat)
        print(pnt)
        serializer.save(location=pnt)


def add_pitch_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")

        if name and address:
            try:
                # Get latitude and longitude from the address
                location = geolocator.geocode(address)
                if location:
                    lat = location.latitude
                    lng = location.longitude
                    point = Point(lng, lat)

                #Save the new Pitch with location
                    Pitch.objects.create(name=name, address=address, location=point)
                    messages.success(request, "Pitch added successfully!")
                    return redirect("homepage")
                else:
                    messages.error(request, "Unable to determine the location for the provided address.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Both name and address fields are required.")

    return render(request, "add_pitch.html")


# from django.http import HttpResponse
# from django.conf import settings
# import os
# from django.views.generic import View

# class ServiceWorkerView(View):
#     def get(self, request, *args, **kwargs):
#         sw_path = os.path.join(settings.BASE_DIR, 'static', 'service-worker.js')
#         try:
#             with open(sw_path, 'rb') as f:
#                 sw_content = f.read()
#             response = HttpResponse(sw_content, content_type='application/javascript')
#             response['Cache-Control'] = 'no-cache'
#             return response
#         except FileNotFoundError:
#             return HttpResponse('Service Worker not found.', status=404)

