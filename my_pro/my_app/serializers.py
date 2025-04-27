from rest_framework import serializers
from .models import QueryLog

class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = '__all__'
