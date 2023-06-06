import dorsaPylon
from dorsaPylon import Collector, Camera



collector = Collector()
#enable camera emulation and pass your ideal camera counts
collector.enable_camera_emulation(2)
#get avialble cameras in class of emlulation
cameras = collector.get_all_cameras(camera_class=dorsaPylon.CamersClass.emulation)
cam1 = cameras[0]
#-----------------------------------------------------------------
cam1.Parms.set_gain(50)
cam1.Operations.start_grabbing()
    