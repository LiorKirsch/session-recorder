from django.db import models
from django.forms.models import model_to_dict
from django.db.models import F
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
import os
import random, string

from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES,
                                default='python',
                                max_length=100)
    style = models.CharField(choices=STYLE_CHOICES,
                             default='friendly',
                             max_length=100)

    class Meta:
        ordering = ('created',)
        

def get_path(instance, filename):
    fileName, fileExtension = os.path.splitext(filename)
    return "images/%s/%s" % (instance.timestamp, filename)

class Document(models.Model):
    timestamp = models.CharField(max_length=20, blank=True, null=True)
    docfile = models.FileField(upload_to=get_path)
    
        

def generateRandomString():
    N = 15
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
 

class Recording_session(models.Model):
    recording_session_id = models.CharField(max_length=15, default= generateRandomString )
    description = models.CharField(max_length=1000, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True, blank=True)
    last_update_date = models.DateTimeField(auto_now_add=True, blank=True)
    total_duration = models.IntegerField(default=0)
    gps_lat = models.FloatField(blank=True, null=True)
    gps_lng = models.FloatField(blank=True, null=True)
   
    users = models.ManyToManyField( User ,blank=True)
    
    created_video_path = models.FilePathField(blank=True, null=True)
    
#    def is_same_configuration(self, configuration):
#        same_conf = self.config_check_wifi_interval == configuration['check_wifi_interval'] 
#        same_conf = same_conf and (self.config_make_server_connection_interval == configuration['make_server_connection_interval'])
#        
#        return same_conf
#        
        
    def __unicode__(self):
        output = '%s - %s' % (self.description, self.recording_session_id)
        return output

        
def get_image_path(instance, filename):
    fileName, fileExtension = os.path.splitext(filename)
    session_obj = instance.recording_session
    
    dateTime = instance.creation_date_client.strftime('%Y-%m-%d_%H_%M')
    fileName = "%s%s" % (dateTime,fileExtension)
    return "images/%s/%s" % (session_obj.recording_session_id, fileName)

class Image(models.Model):
    creation_date_server = models.DateTimeField(auto_now_add=True, blank=True)
    creation_date_client = models.DateTimeField(blank=True)
    time_in_session = models.IntegerField(blank=True, null=True)
    creating_user = models.ForeignKey( User ,blank=True)
    recording_session = models.ForeignKey( Recording_session )
    gps_lat = models.FloatField(blank=True, null=True)
    gps_lng = models.FloatField(blank=True, null=True)
    
    image_file = models.ImageField(upload_to=get_image_path)
           
    def get_str(self):
        return model_to_dict(self, fields=['file_path','time_in_session','creation_date_client'])

    def __unicode__(self):
        output = "%s - %s" % (self.creation_date_server, self.recording_session)
        return output

def get_audio_path(instance, filename):
    fileName, fileExtension = os.path.splitext(filename)
    session_obj = instance.recording_session
    
    dateTime = instance.creation_date_client.strftime('%Y-%m-%d-%H-%M')
    fileName = "%s%s" % (dateTime,fileExtension)
    return "audio/%s/%s" % (session_obj.recording_session_id, fileName)

class Audio(models.Model):
    creation_date_server = models.DateTimeField(auto_now_add=True, blank=True)
    creation_date_client = models.DateTimeField(blank=True)
    time_in_session = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    gps_lat = models.FloatField(blank=True, null=True)
    gps_lng = models.FloatField(blank=True, null=True)  

    creating_user = models.ForeignKey( User ,blank=True)
    recording_session = models.ForeignKey( Recording_session )
    
    file_path = models.FileField(upload_to=get_audio_path)
        

    def get_str(self):
        return model_to_dict(self, fields=['file_path','time_in_session','creation_date_client'])

    def __unicode__(self):
        output = "%s - %s" % (self.creation_date_server, self.recording_session)
        return output
 