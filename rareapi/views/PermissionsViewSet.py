from rest_framework import status
from rest_framework.response import Response
from rest_framework import status
from rareapi.models import RareUser, DemotionQueue
from rest_framework.decorators import api_view
import json
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied

@api_view()
def check_active(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
    request -- The full HTTP request object
    '''
    rare_user = RareUser.objects.get(user = request.auth.user)
    data = json.dumps({"is_active": request.auth.user.is_active, "is_admin": request.auth.user.is_staff, "logged_in_user_id": rare_user.id})
    return HttpResponse(data, content_type='application/json')

@api_view(["PUT"])
def change_active(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
    request -- The full HTTP request object
    '''
    if not request.auth.user.has_perm('rareapi.change_rareuser'):
        raise PermissionDenied()
    rare_user = RareUser.objects.get(user=request.data['user_id'])
    admin_rare_user = RareUser.objects.get(user=request.auth.user)
    if request.data["action"] == "deactivate":
        try:
            is_in_queue = DemotionQueue.objects.get(user=rare_user, action=request.data["action"], approver__isnull=True)
            if admin_rare_user.id is not is_in_queue.admin_id:
                is_in_queue.approver = admin_rare_user
                is_in_queue.save()
                rare_user.user.is_active = False
                rare_user.user.save()
                data = json.dumps({"status": "deactivated"})
                return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)
            else:
                raise PermissionDenied()
        except DemotionQueue.DoesNotExist:
            is_in_queue = DemotionQueue()
            is_in_queue.user = rare_user
            is_in_queue.admin = admin_rare_user
            is_in_queue.action = request.data["action"]
            is_in_queue.save()
            data = json.dumps({"status": "queued"})
            return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)
    elif request.data["action"] == "activate":
        rare_user.user.is_active = True
        rare_user.user.save()
        data = json.dumps({"status": "activated"})
        return HttpResponse(data, content_type='application/json', status=status.HTTP_200_OK)

@api_view(["PUT"])
def change_rank(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
    request -- The full HTTP request object
    '''
    if not request.auth.user.has_perm('rareapi.change_rareuser'):
        raise PermissionDenied()
    rare_user = RareUser.objects.get(user=request.data['id'])
    rare_user.user.is_staff = request.data['isAdmin']
    rare_user.user.save()
    if request.data['isAdmin']:
        permissions = [46, 48, 33, 34, 35, 49, 50, 51, 57, 58, 59]
        rare_user.user_permissions.set(permissions)
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    rare_user.user.user_permissions.clear()
    return Response({}, status=status.HTTP_204_NO_CONTENT)
