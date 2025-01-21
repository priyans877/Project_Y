from rest_framework import serializers
from scrap.models import result


class resultSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = result
        fields = '__all__'
