'''
Created on Sep 4, 2014

@author: lior
'''

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from models import Recording_session, Image, Audio

from django.forms import widgets
from models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES


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
    

class SnippetSerializer(serializers.Serializer):
    pk = serializers.Field()  # Note: `Field` is an untyped read-only field.
    title = serializers.CharField(required=False,
                                  max_length=100)
    code = serializers.CharField(widget=widgets.Textarea,
                                 max_length=100000)
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES,
                                       default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES,
                                    default='friendly')

    def restore_object(self, attrs, instance=None):
        """
        Create or update a new snippet instance, given a dictionary
        of deserialized field values.

        Note that if we don't define this method, then deserializing
        data will simply return a dictionary of items.
        """
        if instance:
            # Update existing instance
            instance.title = attrs.get('title', instance.title)
            instance.code = attrs.get('code', instance.code)
            instance.linenos = attrs.get('linenos', instance.linenos)
            instance.language = attrs.get('language', instance.language)
            instance.style = attrs.get('style', instance.style)
            return instance

        # Create new instance
        return Snippet(**attrs)