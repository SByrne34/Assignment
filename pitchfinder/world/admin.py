from leaflet.admin import LeafletGeoAdmin
from django.contrib.gis import admin
from .models import WorldBorder
from .models import Pitch

@admin.register(WorldBorder)
class WorldBorderAdmin(LeafletGeoAdmin):
    pass

@admin.register(Pitch)
class HotelAdmin(LeafletGeoAdmin):
    list_display = ("id", "name", "address", "location", "created_at", "updated_at")
