from django.http.response import HttpResponse
from rareapi.models import Category, Reaction
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.core.files.base import ContentFile
import base64
import uuid
from django.core.exceptions import PermissionDenied

class ReactionViewSet(ViewSet):
    def create(self, request):
        # Create a new instance of the reaction picture model you defined
        if not request.auth.user.has_perm('rareapi.add_reaction'):
            raise PermissionDenied()

        reaction = Reaction()

        format, imgstr = request.data["image_url"].split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{request.data["label"]}-{uuid.uuid4()}.{ext}')

        reaction.image_url = data
        reaction.label = request.data["label"]        

        try:
            reaction.save()
            serializer = ReactionSerializer(reaction, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception:
            return HttpResponse(Exception)
        
    def list(self, request):
        reactions = Reaction.objects.all()
        serializer = ReactionSerializer(reactions, many=True, context={'request': request})

        return Response(serializer.data)

class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'label', 'image_url')