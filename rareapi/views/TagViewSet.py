from django.http.response import HttpResponse
from rareapi.models import Tag
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

class TagViewSet(ViewSet):
    def create(self, request):
        tag = Tag()

        tag.label = request.data["label"]

        try:
            tag.save()
            serializer = TagSerializer(tag, context={'request', request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return HttpResponse(Exception)

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id","label")