from django.urls import path
from .views import (
    homepage,
    map_view,
    login_view,
    logout_view,
    update_location,
    ListCreateGenericViews,
    PitchUpdateRetreiveView,
    add_pitch_view,
)

urlpatterns = [
    path('', homepage, name='homepage'),
    path('map/', map_view, name='map'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('update_location/', update_location, name='update_location'),
    path('api/pitches/', ListCreateGenericViews.as_view(), name='pitch-list-create'),
    path('pitches/<int:pk>/', PitchUpdateRetreiveView.as_view(), name='pitch-detail'), 
    path("pitches/add", add_pitch_view, name="add_pitch"),  
]

