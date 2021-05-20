from rareapi.models.Post import Post
from django.http.response import HttpResponse
from rareapi.models import RareUser, PostReaction, Post, Reaction
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User

class PostReactionViewSet(ViewSet):
    def create(self, request):
        post_reaction = PostReaction()
        user = RareUser.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post_id"])
        reaction = Reaction.objects.get(pk=request.data["reaction_id"])
        post_reaction.post = post
        post_reaction.user = user
        post_reaction.reaction = reaction
        try:
            post_reaction.save()
            serializer = PostReactionSerializer(post_reaction, context={'request', request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception:
            post_reaction = PostReaction.objects.get(user=user,post=post,reaction=reaction)
            post_reaction.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        try:
            post_reaction = PostReaction.objects.get(pk=pk)
            post_reaction.delete()
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return HttpResponse(Exception)
class PostReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostReaction
        fields = ('__all__')   