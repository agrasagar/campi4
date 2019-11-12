import os
import pygame, sys

from pygame.locals import *
import pygame.camera

class Cam:
    def __init__(self, name):
        self.name = name
        self.size = (640, 480)
        self.supported_colorspace = ["RGB", "YUV", "HSV"]
        pygame.init()
        pygame.camera.init()
   
    def __snap(self, image_filename, cam_number, colorSpace="RGB"):
        try:
            self.cam = pygame.camera.Camera("/dev/video{}".format(cam_number), self.size, colorSpace)
            self.cam.start()
            image = self.cam.get_image()
            pygame.image.save(image, image_filename)
        except SystemError as e:
            return ("FAIL", repr(e))
        except AttributeError as e:
            return ("FAIL", repr(e))
        except Exception as e:
            self.cam.stop()
            return ("FAIL", repr(e))
        self.cam.stop()
        return ("SUCCESS", image_filename)
        
    def take_snap(self, cam_number, colorSpace):
        image_filename = "image{}.jpg".format(cam_number)
        return self.__snap(image_filename
                        , cam_number
                        , colorSpace)
    
