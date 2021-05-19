
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rareapi.models import Post, Category, RareUser
from django.contrib.auth.models import Permission, User
from django.db.models import Q
from rest_framework.decorators import api_view
import json
from django.http import HttpResponse

@api_view()
def check_active(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
    request -- The full HTTP request object
    '''

    data = json.dumps({"is_active": request.auth.user.is_active, "is_admin": request.auth.user.is_staff})
    return HttpResponse(data, content_type='application/json')

@api_view(["PUT"])
def change_active(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
    request -- The full HTTP request object
    '''

    rare_user = RareUser.objects.get(user=request.data['user_id'])
    if request.data["action"] == "deactivate":
        rare_user.user.is_active = False
        rare_user.user.is_staff = False
        rare_user.user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    elif request.data["action"] == "activate":
        rare_user.user.is_active = True
        rare_user.user.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)