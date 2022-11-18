from rest_framework import serializers
from . models import Election_Area, Details, Main

class detailserializer(serializers.ModelSerializer):
    class Meta:
        model = Details
        fields = ['id','name','party','vote','area']
        
class easerializers(serializers.ModelSerializer):
    candidates = detailserializer(many=True)
    class Meta:
        model= Election_Area
        fields = ['id','election_area','candidates']
        depth = 2
        
class mainserializer(serializers.ModelSerializer):
    data = easerializers(many=True)
    class Meta:
        model = Main
        fields = ['id','updated_time','data']
        