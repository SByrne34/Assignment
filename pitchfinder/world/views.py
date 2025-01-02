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
# from django.http import HttpResponse
# from django.conf import settings
# import os
# from django.views.generic import View

# View that provides the homepage of pitchfinder
def homepage(request):
    return render(request, 'homepage.html')  

# View that provides the map for the pitches and live location
# User login is required to operate map page
@login_required
def map_view(request):
    try:
        # User profile is required to obtain live location
        user_profile = Profile.objects.get(user=request.user)
        location = user_profile.location
        # Sets live location to default if no user profile is present
    except Profile.DoesNotExist:
        location = None

    return render(request, 'map.html', {'user': request.user, 'location': location})

# View that provides updated location when button is clicked
def update_location(request):   
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        user = request.profile
        user.location = Point(float(longitude), float(latitude))
        user.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# View that provides the login page for pitchfinder
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

# View that provides the ability to log out and redirects to login page
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

# View that provides a pitch addition system that is present in admin and rest framework
def add_pitch_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        address = request.POST.get("address")

        if name and address:
            try:
                # The address given will have the lng and lat calulcated
                location = geolocator.geocode(address)
                if location:
                    lat = location.latitude
                    lng = location.longitude
                    point = Point(lng, lat)

                # The pitch is then saved alongside the location entered for it
                    Pitch.objects.create(name=name, address=address, location=point)
                    messages.success(request, "Pitch has been added!")
                    return redirect("homepage")
                # Provides an error if the location provided is not accurate enough
                else:
                    messages.error(request, "Can't find the location of the address provided.")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        # Both values need to be entered for details to be saved
        else:
            messages.error(request, "You need to enter both the address and the name.")

    return render(request, "add_pitch.html")



# View for service worker which provides offline functionality when uncommented
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
#             return HttpResponse('Service Worker cannot be found', status=404)

