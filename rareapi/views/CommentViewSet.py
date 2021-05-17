from rareapi.models.Post import Post
from django.http.response import HttpResponse
from rareapi.models import Category, Comment, RareUser
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status

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

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"