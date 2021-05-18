from django.http.response import HttpResponse
from rareapi.models import Category
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class CategoryViewSet(ViewSet):
    def create(self, request):
        category = Category()
        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request', request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return HttpResponse(Exception)
    
    def list(self, request):
        # TODO: admin-only endpoint
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return HttpResponse(Exception)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'