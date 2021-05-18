from django.http.response import HttpResponse
from rareapi.models import Category, RareUser
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers

class CategoryViewSet(ViewSet):
    def create(self, request):
        category = Category()
        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request', request})
            return Response(serializer.data)
        except Exception:
            return HttpResponse(Exception)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'