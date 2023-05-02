from django.shortcuts import render
import cv2
from django.http import StreamingHttpResponse
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from django.http import HttpResponse
from django.views.decorators import gzip
import numpy as np
# import some common detectron2 utilities
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer , ColorMode
from detectron2.data import MetadataCatalog

# Create your views here.
class Detector:

    def __init__(self):
        self.cfg = get_cfg()

        self.cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml"))
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_101_FPN_3x.yaml")

        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
        self.cfg.MODEL.DEVICE = "cpu"

        self.predictor = DefaultPredictor(self.cfg)
    
    def onVideo(self,frame):
        predictiions = self.predictor(frame)

        viz = Visualizer(frame[:,:,::-1],metadata = MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]),
                        instance_mode = ColorMode.IMAGE_BW)
        
        output = viz.draw_instance_predictions(predictiions["instances"].to("cpu"))

        return output


# def detect_image(request):
#     return render(request,'detectron.html')
# Define a function to capture video from the camera

def generate_frames():
    cap = cv2.VideoCapture(0) 
    detector = Detector()
    while True:
        ret, frame = cap.read()

        if not ret:
            break
        else:
            output = detector.onVideo(frame)
            # Encode the frame as a jpeg image and yield it
            ret, buffer = cv2.imencode('.jpg', output.get_image()[:,:,::-1])
            output = buffer.tobytes()
            yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + output + b'\r\n')
            

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            ret, frame = cap.read()

        

        

    cap.release()

def detect_video(request):
    return StreamingHttpResponse(generate_frames(),content_type='multipart/x-mixed-replace; boundary=frame')
   