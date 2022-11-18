from django.contrib import admin

from .models import Details, Election_Area, Main

# Register your models here.
@admin.register(Election_Area)
class Area(admin.ModelAdmin):
    list_display = ['election_area']
    
@admin.register(Details)
class Data(admin.ModelAdmin):
    list_display = ['name','party','vote']
    
@admin.register(Main)
class Main(admin.ModelAdmin):
    list_display= ['updated_time']