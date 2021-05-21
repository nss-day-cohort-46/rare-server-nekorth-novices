
from rareapi.models.Subscription import Subscription
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, Category, RareUser, Tag, Comment, PostReaction
from django.contrib.auth.models import User
from django.db.models import Q
from .TagViewSet import TagSerializer
from .CategoryViewSet import CategorySerializer
from django.core.files.base import ContentFile
import base64
import uuid
from rest_framework.decorators import action

# CHECK SERIALIZERS SEE IF CAN REUSE THE COMMENT SERIALIZER
class PostViewSet(ViewSet):
    def create(self, request):
        rareuser = RareUser.objects.get(user=request.auth.user)
        post = Post()
        post.title = request.data["title"]
        post.user = rareuser
        post.content = request.data["content"]
        if request.data["image_url"] :
            format, imgstr = request.data["image_url"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["title"]}-{uuid.uuid4()}.{ext}')
            post.image_url = data
        if request.data["category_id"] is not 0 :
            category = Category.objects.get(pk=request.data["category_id"])
            post.category = category
        try:
            post.save()
            tags = Tag.objects.in_bulk(request.data["tag_ids"])
            post.tag_set.set(tags)
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
        if request.data["image_url"] :
            format, imgstr = request.data["image_url"].split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["title"]}-{uuid.uuid4()}.{ext}')
            post.image_url = data
        if request.data["category_id"] is not 0 :
            category = Category.objects.get(pk=request.data["category_id"])
            post.category = category
        post.tag_set.set(request.data["tag_ids"])
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
        search_term = self.request.query_params.get('q', None)
        search_category = self.request.query_params.get('category', None)
        user_id = self.request.query_params.get('user_id', None)
        user = self.request.query_params.get('user', None)
        rareuser = RareUser.objects.get(user = request.auth.user)
        if user is not None:
            posts = posts.filter(user = RareUser.objects.get(pk=user))
        if user_id is not None:
            posts = posts.filter(user = rareuser)
        if search_category is not None:
            category = Category.objects.get(pk=search_category)
            posts = posts.filter(category = category)
        if search_term is not None:
            posts = posts.filter(Q(title__contains=search_term) | Q(tag__label__contains=search_term))
        for post in posts:
            post.ownership = rareuser
        serializer = PostSerializer(
            posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False)
    def subscribed_posts(self, request):
        subscribed_posts = []
        subscriptions = Subscription.objects.filter(follower=request.auth.user.id, ended_on = None)
        for subscription in subscriptions:
            user_posts = Post.objects.filter(user=subscription.author)
            for post in user_posts:
                subscribed_posts.append(post)

        serializer = PostSerializer(subscribed_posts, many=True, context={'request': request})
        return Response(serializer.data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)
class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = RareUser
        fields = ('user', 'bio')
class CommentSerializer(serializers.ModelSerializer):
    author = RareUserSerializer(many=False)
    class Meta:
        model = Comment
        fields = "__all__" 
class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('__all__')         
class PostSerializer(serializers.ModelSerializer):
    user = RareUserSerializer(many=False)
    category = CategorySerializer(many=False)
    tag_set = TagSerializer(many=True)
    comment_set = CommentSerializer(many=True)
    postreaction_set = PostReactionSerializer(many=True)
    class Meta:
        model = Post
        fields = ('id', 'title','user','content','image_url','publication_date','approved','tag_set', 'category', 'comment_set', 'ownership','postreaction_set')