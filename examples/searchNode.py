import dorsaPylon
from dorsaPylon import Collector, Camera
import cv2


collector = Collector()
collector.enable_camera_emulation(2)
cameras = collector.get_all_cameras(camera_class=dorsaPylon.CamersClass.emulation)
cam1 = cameras[0]
#-----------------------------------------------------------------
nodes_name = cam1.search_in_nodes('gain')
print(f'first nodes name is {nodes_name[0]}')

cam1.Parms.set_node('GainRaw', 195)
gain = cam1.Parms.get_node('GainRaw')
print(f'gain set {gain}')

#-----------------------------------------------------------------
node_name = 'ExposureMode'
possible_values = cam1.Parms.availble_node_values(node_name)
print(f'possible values for {node_name} are: {possible_values}')
