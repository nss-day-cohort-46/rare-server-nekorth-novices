from django.http.response import HttpResponse
from rareapi.models import Category
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.exceptions import PermissionDenied

class CategoryViewSet(ViewSet):
    def create(self, request):
        # TODO: Add unique constraint to label property on model?
        if not request.auth.user.has_perm('rareapi.add_category'):
            raise PermissionDenied()

        category = Category()
        category.label = request.data["label"]

        try:
            category.save()
            serializer = CategorySerializer(category, context={'request', request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return HttpResponse(Exception)
    
    def list(self, request):
        # TODO: admin-only endpoint?
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        # TODO: admin-only endpoint
        if not request.auth.user.has_perm('rareapi.delete_category'):
            raise PermissionDenied()
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return HttpResponse(Exception)
    
    def update(self, request, pk):
        # TODO: admin-only endpoint
        if not request.auth.user.has_perm('rareapi.change_category'):
            raise PermissionDenied()

        category = Category.objects.get(pk=pk)

        category.label = request.data["label"]

        try:
            category.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return HttpResponse(Exception)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'