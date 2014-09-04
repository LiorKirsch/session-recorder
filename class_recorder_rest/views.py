from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics ,response
from class_recorder_rest.serializers import UserSerializer, GroupSerializer, ImageSerializer, RecordingSessionSerializer, AudioSerializer
from models import Recording_session, Image, Audio

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.shortcuts import get_object_or_404
from rest_framework.response import Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


#class GroupViewSet(viewsets.ModelViewSet):
#    queryset = Group.objects.all()
#    serializer_class = GroupSerializer
#    
    
class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    
class AudioViewSet(viewsets.ModelViewSet):
    queryset = Audio.objects.all()
    serializer_class = AudioSerializer
    
class RecordingSessionViewSet(viewsets.ModelViewSet):
    queryset = Recording_session.objects.all()
    serializer_class = RecordingSessionSerializer


class RecordingSessionDetailView(generics.ListAPIView):
    serializer_class = RecordingSessionSerializer
    lookup_field = 'recording_session_id'
    
    def get_queryset(self):
        session_id = self.kwargs['session_id']
        return Recording_session.objects.filter(recording_session_id=session_id)
    