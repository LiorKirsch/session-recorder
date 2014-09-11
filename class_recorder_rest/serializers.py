'''
Created on Sep 4, 2014

@author: lior
'''

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import Recording_session, Image, Audio

from django.forms import widgets


class HyperlinkedFileField(serializers.FileField): 
    def to_native(self, value): 
        request = self.context.get('request', None) 
        return request.build_absolute_uri(value.url) 
    
class HyperlinkedThumbnail(serializers.URLField): 
    def to_native(self, value): 
        request = self.context.get('request', None) 
        return request.build_absolute_uri(value.thumbnail.url) 


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
        
class ImageSerializer(serializers.HyperlinkedModelSerializer):
#    thumbnail_file = serializers.Field(source='thumbnail_file')
    image_file = HyperlinkedFileField(source='image_file')
    thumbnail = HyperlinkedThumbnail(source='image_file', read_only=True, required=False)
    
    class Meta:
        model = Image
        fields = ('url', 'creation_date_server', 'creation_date_client', 'time_in_session','creating_user', 'recording_session',
                  'gps_lat','gps_lng','image_file','thumbnail')
       
                
class AudioSerializer(serializers.HyperlinkedModelSerializer):
    duration = serializers.Field(source='duration')
    audio_file = HyperlinkedFileField(source='file_path')
    
    class Meta:
        model = Audio
        fields = ('url', 'creation_date_server', 'creation_date_client', 'time_in_session','creating_user', 'recording_session',
                  'gps_lat','gps_lng','audio_file','duration')     
        
               
class RecordingSessionSerializer(serializers.ModelSerializer):
    recording_session_id = serializers.Field(source='recording_session_id')
    images = ImageSerializer(many=True)
    audios = AudioSerializer(many=True)
    
    class Meta:
        model = Recording_session
        fields = ('recording_session_id', 'description', 'creation_date','last_update_date', 'total_duration',
                  'gps_lat','gps_lng','users','created_video_path','images','audios')
       