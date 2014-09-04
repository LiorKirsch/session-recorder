from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics ,response
from class_recorder_rest.serializers import UserSerializer, GroupSerializer, ImageSerializer, SnippetSerializer, RecordingSessionSerializer, AudioSerializer
from models import Recording_session, Image, Audio, Snippet

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
    
    
class SnippetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def snippet_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetSerializer(snippets, many=True)
        return JSONResponse(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data, status=201)
        return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = SnippetSerializer(snippet)
        return JSONResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JSONResponse(serializer.data)
        return JSONResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)