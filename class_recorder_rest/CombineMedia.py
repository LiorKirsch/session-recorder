'''
Created on Aug 31, 2014

@author: lior
'''

import os, cgi, shutil, glob
import subprocess
from threading import Thread
import time
import json
import re

try:    
    import thread 
except ImportError:
    import _thread as thread #Py3K changed it.
 
 
class CombineMedia(object):
    '''
    This class handle all the combination of images and sound into a single video
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def combineImagesAndSound(self, working_folder, sound_path, images_path, images_time_points):
        '''
        Combine a single audio file with images files using ffmpeg
        '''
        
        fileName = generateRandomString(10)
        output_folder = folder + fileName
        print("Creating movie: %s" % outputFileName)


        coderCommand = "mencoder mf://%s/*.jpeg -mf w=%s:h=%s:fps=%s:type=jpeg -ovc copy -oac copy -o %s" % (working_folder, resolution[0], resolution[1], framesPerSecond, outputFileName)
#        coderCommand = "mencoder mf://%s/*.jpeg -mf w=%s:h=%s:fps=%s:type=jpeg -ovc lavc -lavcopts vcodec=mpeg4:mbd=2:trell -oac copy -o %s" % (folder, resolution[0], resolution[1], framesPerSecond, outputFileName)

        proc = subprocess.Popen( coderCommand.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Thread(target=self.stream_watcher, name='stdout-watcher', args=('STDOUT', proc.stdout)).start()
        Thread(target=self.stream_watcher, name='stderr-watcher', args=('STDERR', proc.stderr)).start()
        #(output, error) = proc.communicate()
        #print("Output:\n%s" % output)
        #print("Errors:\n%s" % error)
        proc.wait()
        print('done creating movie %s' % outputFileName)
        self.server.encodingInProgress = False
        return outputFileName
        
    
    def generateRandomString(N):
        return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(N))
    