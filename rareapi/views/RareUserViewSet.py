from django.http.response import HttpResponse
from rareapi.models import RareUser
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseServerError

class RareUserViewSet(ViewSet):
    def retrieve(self, request, pk):
        try:
            user = RareUser.objects.get(pk=pk)
            serializer = RareUserSerializer(user, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    #only returns list of active users
    def list(self, request):
        if not request.auth.user.has_perm('rareapi.view_rareuser'):
            raise PermissionDenied()
        users = RareUser.objects.order_by('user__first_name').exclude(user=request.user).exclude(user__is_active=False)
        serializer = RareUserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'is_staff', 'is_active', 'email')

class RareUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)
    class Meta:
        model = RareUser
        fields = ('user', 'bio', 'id', 'profile_image', 'created_on')