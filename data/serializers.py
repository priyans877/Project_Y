from rest_framework import serializers
from scrap.models import result


class resultSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    class Meta:
        model = result
        fields = '__all__'
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = result
        fields = '__all__'
