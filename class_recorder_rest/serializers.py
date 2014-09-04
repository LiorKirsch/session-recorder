'''
Created on Sep 4, 2014

@author: lior
'''

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import Recording_session, Image, Audio

from django.forms import widgets


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
        
class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ('url', 'creation_date_server', 'creation_date_client', 'time_in_session','creating_user', 'recording_session',
                  'gps_lat','gps_lng','image_file')     
        
                
class AudioSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Audio
        fields = ('url', 'creation_date_server', 'creation_date_client', 'time_in_session','creating_user', 'recording_session',
                  'gps_lat','gps_lng','file_path')     
        
           
class RecordingSessionSerializer(serializers.HyperlinkedModelSerializer):
    recording_session_id = serializers.Field(source='recording_session_id')
    
    class Meta:
        model = Recording_session
        fields = ('url', 'recording_session_id', 'description', 'creation_date','last_update_date', 'total_duration',
                  'gps_lat','gps_lng','users','created_video_path')     
    