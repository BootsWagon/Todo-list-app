from rest_framework import serializers
from .models import Theme

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['theme_data'] 