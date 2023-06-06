import dorsaPylon
from dorsaPylon import Collector, Camera


collector = Collector()

#get avialble cameras That Are GigE
gige_cameras = collector.get_all_cameras(camera_class=dorsaPylon.CamersClass.gige)

#-----------------------------------------------------------------
#get all avialble cameras 
all_cameras = collector.get_all_cameras(camera_class=None)

#-----------------------------------------------------------------
#get specific camera
cam = collector.get_camera_by_serial('123456')