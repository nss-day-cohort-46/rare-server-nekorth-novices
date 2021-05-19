from django.http.response import HttpResponse
from rest_framework.decorators import action
from rareapi.models import RareUser, Subscription
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError
from rest_framework import status
from django.utils import timezone

class RareUserViewSet(ViewSet):
    # def create(self, request):
    #     rareuser = RareUser.objects.get(user=request.auth.user)
    #     post = Post()
    #     post.title = request.data["title"]
    #     post.user = rareuser
    #     post.content = request.data["content"]
    #     if request.data["category_id"] is not 0 :
    #         category = Category.objects.get(pk=request.data["category_id"])
    #         post.category = category
    #     try:
    #         post.save()
    #         serializer = PostSerializer(post, context={'request': request})
    #         return Response(serializer.data)
    #     except ValidationError as ex:
    #         return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
    def retrieve(self, request, pk):
        try:
            user = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    # def update(self, request, pk=None):
    #     rareuser = RareUser.objects.get(user=request.auth.user)
    #     post = Post.objects.get(pk=pk)
    #     post.title = request.data["title"]
    #     post.user = rareuser
    #     post.content = request.data["content"]
    #     if request.data["category_id"] is not 0 :
    #         category = Category.objects.get(pk=request.data["category_id"])
    #         post.category = category
    #     post.save()
    #     return Response({}, status=status.HTTP_204_NO_CONTENT)
    # def destroy(self, request, pk=None):
    #     try:
    #         post = Post.objects.get(pk=pk)
    #         post.delete()
    #         return Response({}, status=status.HTTP_204_NO_CONTENT)
    #     except Post.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
    #     except Exception as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def list(self, request):
        if not request.auth.user.has_perm('rareapi.view_rareuser'):
            raise PermissionDenied()
        users = RareUser.objects.order_by('user__first_name').exclude(user=request.user)
        serializer = RareUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=["post", "delete" ], detail=False)
    def subscription(self, request):
        author = RareUser.objects.get(pk=request.data["author_id"])
        follower = RareUser.objects.get(user=request.auth.user)

        if request.method == "POST":
            subscription = Subscription()
            subscription.author = author
            subscription.follower = follower
            try:
                subscription.save()
            # serializer = SubscriptionSerializer(subscription, many=False, conext={'request': request})
                return Response({}, status=status.HTTP_201_CREATED)
            except Exception:
                return HttpResponseServerError(Exception)
        elif request.method == "DELETE":
            try:
                subscription = Subscription.objects.get(author=author, follower=follower, ended_on=None)
                subscription.ended_on = timezone.now()
                subscription.save()
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Exception:
                return HttpResponseServerError(Exception)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'is_staff', 'is_active', 'email')

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = RareUser
        fields = ('user', 'bio', 'id', 'profile_image', 'created_on')

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'