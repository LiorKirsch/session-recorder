from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics ,response
from class_recorder_rest.serializers import UserSerializer, GroupSerializer, ImageSerializer, RecordingSessionSerializer, AudioSerializer
from models import Recording_session, Image, Audio
from django.conf import settings

import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import json 

from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from mutagen.mp3 import MP3


from PIL import Image as PIL_Image
    
def build_video(request, session_id):
    '''
    Using the lecture id it searches for media files in the folder 
    Then build a video using the images and sound
    '''
     
    current_user = request.user
    data=json.loads( request.body )
    lecture_id = data['lecture_id']
    working_folder = lecture_id
    
    video_file_path = CombineMedia.combineImagesAndSound(working_folder, sound_path, images_path, images_time_points)
    
    output = {}

    return sendObjectAsJson(output)

def build_slideshow(request, session_id):
    '''
    Using the session id it searches for media files in the folder 
    Then build returns a json which contains information about the slideshow
    '''
    session = Recording_session.objects.get(recording_session_id=session_id)
    session_images = Image.objects.filter(recording_session=session)

    
    for image_object in session_images:
        print image_object


    session_audio = Audio.objects.get(recording_session=session)

    audio_file = MP3( session_audio.file_path.path )
    duration = audio_file.info.length
    
    working_folder = session_id
    output = {}
    

    return sendObjectAsJson(output)
    

def sendObjectAsJson(myObjectDict):
    data = json.dumps(myObjectDict, indent=4) 
    resp = HttpResponse(data, content_type='application/json')
    resp['Access-Control-Allow-Headers'] = '*'
    return resp

class SessionDetails(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        """
        This view should return a list of all the images for
        the session as determined by the session_id portion of the URL.
        """
        session_id = self.kwargs['session_id']
        return Image.objects.filter(recording_session=session_id)
    
    
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
    

    