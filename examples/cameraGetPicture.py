import dorsaPylon
from dorsaPylon import Collector, Camera
import cv2


collector = Collector()
#enable camera emulation and pass your ideal camera counts
collector.enable_camera_emulation(1)
#get avialble cameras in class of emlulation
camera = collector.get_all_cameras(camera_class=None)[0]
#-----------------------------------------------------------------
#define your ideal pixel_type, defualt is BGR8
camera.build_converter(pixel_type=dorsaPylon.PixelType.GRAY8)
#-----------------------------------------------------------------
img = camera.getPictures()
cv2.imshow('img', img)
cv2.waitKey(0)
