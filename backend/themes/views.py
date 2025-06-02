from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Theme
from .serializers import ThemeSerializer

@api_view(['GET', 'PUT', 'DELETE'])
def theme_detail(request):
    try:
        # For now, we'll use a default theme for all users
        theme = Theme.objects.first()
    except Theme.DoesNotExist:
        if request.method == 'GET':
            return Response(status=status.HTTP_404_NOT_FOUND)
        theme = None

    if request.method == 'GET':
        if not theme:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ThemeSerializer(theme)
        return Response(serializer.data['theme_data'])

    elif request.method == 'PUT':
        if theme:
            serializer = ThemeSerializer(theme, data={'theme_data': request.data})
        else:
            serializer = ThemeSerializer(data={'theme_data': request.data})
            
        if serializer.is_valid():
            theme = serializer.save()
            return Response(theme.theme_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if theme:
            theme.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 