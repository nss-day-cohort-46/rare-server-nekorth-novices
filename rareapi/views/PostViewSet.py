
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, Category, RareUser
from django.contrib.auth.models import User
from django.db.models import Q


class PostViewSet(ViewSet):
    def create(self, request):
        rareuser = RareUser.objects.get(user=request.auth.user)
        post = Post()
        post.title = request.data["title"]
        post.user = rareuser
        post.content = request.data["content"]
        if request.data["category_id"] is not 0 :
            category = Category.objects.get(pk=request.data["category_id"])
            post.category = category
        try:
            post.save()
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    def update(self, request, pk=None):
        rareuser = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=pk)
        post.title = request.data["title"]
        post.user = rareuser
        post.content = request.data["content"]
        if request.data["category_id"] is not 0 :
            category = Category.objects.get(pk=request.data["category_id"])
            post.category = category
        post.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    def destroy(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
            post.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def list(self, request):
        posts = Post.objects.all()
        search_text = self.request.query_params.get('q', None)
        sort_text = self.request.query_params.get('orderby', None)
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = RareUser
        fields = ('user', 'bio')       
class PostSerializer(serializers.ModelSerializer):
    user = RareUserSerializer(many=False)
    class Meta:
        model = Post
        fields = ('id', 'title','user','content','image_url','publication_date','approved')