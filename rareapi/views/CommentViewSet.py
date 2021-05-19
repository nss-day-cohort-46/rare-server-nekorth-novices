from rareapi.models.Post import Post
from django.http.response import HttpResponse
from rareapi.models import Comment, RareUser
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User

class CommentViewSet(ViewSet):
    def create(self, request):
        comment = Comment()
        author = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post_id"])

        comment.post = post
        comment.content = request.data["content"]
        comment.author = author

        try:
            comment.save()
            serializer = CommentSerializer(comment, context={'request', request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            return HttpResponse(Exception)

    def destroy(self, request, pk):
        # TODO: only the comment creator should be able to delete

        try:
            comment = Comment.objects.get(pk=pk)
            comment.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return HttpResponse(Exception)
    
    def update(self, request, pk):
        # TODO: only creator should be able to edit
        comment = Comment.objects.get(pk=pk)

        comment.content = request.data["content"]

        try:
            comment.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return HttpResponse(Exception)

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