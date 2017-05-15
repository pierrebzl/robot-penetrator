import time
import io
import threading
import picamera
import sys
import re
import subprocess
import cv2

from io import StringIO
from importlib import import_module
#from PIL import Image

env = sys.argv[1] if len(sys.argv) == 2 else 'default'
config = import_module('conf.%s' % env).config


def list_camera_ids():
    cameras = subprocess.Popen(['ls', '/dev/video*'], stdout=subprocess.PIPE).communicate()[0]
    return re.findall(r'\d+', cameras)

class Camera(object):
    def __init__(self, camera_id, size, fps):
        self.cam = cv2.VideoCapture(int(camera_id))
        self.cam.set(cv2.CAP_PROP_FPS, fps)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, size[0])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, size[1])

    def get_frame(self):
        if not self.cam.isOpened():
            return ''

        ret, frame = self.cam.read()
        image = Image.fromarray(frame)
        buf = StringIO()
        image.save(buf, 'JPEG')

        return buf.getvalue()

    '''thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.annotate_text = config['CAMERA_TEXT']
            camera.resolution = (config['H_PIC'], config['V_PIC'])
            camera.hflip = True
            camera.vflip = True

            # let camera warm up
            camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):
                # store frame
                stream.seek(0)
                cls.frame = stream.read()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None'''
