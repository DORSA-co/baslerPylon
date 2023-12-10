import sys
import os
sys.path.append( os.getcwd())


import dorsaPylon
from dorsaPylon import Collector, Camera


collector = Collector()
#enable camera emulation and pass your ideal camera counts
collector.enable_camera_emulation(1)
#get avialble cameras in class of emlulation
camera = collector.get_all_cameras(camera_class=dorsaPylon.CamersClass.emulation)[0]
#-----------------------------------------------------------------
model = camera.Infos.get_model()
print(f'model: {model}')

serial = camera.Infos.get_serialnumber()
print(f'serial: {serial}')

is_gige = camera.Infos.is_GigE()
print(f'is camera GigE: {is_gige}')
#-----------------------------------------------------------------
#Parms is useing for set camera options
camera.Parms.set_gain(50)
gain = camera.Parms.get_gain()
print(f'gain is {gain}')

camera.Parms.set_trigger_on()
trigger = camera.Parms.get_trigger_mode()
print(f'trgigger is {trigger}')

possible_triggersource_value = camera.Parms.availble_triggersource_values()
print(f'possible trigger source values are:{possible_triggersource_value}')

camera.Parms.set_trigger_option(dorsaPylon.Trigger.source.software,
                                dorsaPylon.Trigger.selector.frame_start
                                )

#-----------------------------------------------------------------

camera.Parms.set_exposureTime(2000)
exposure = camera.Parms.get_exposureTime()
print(f'exposure is {exposure}')
#-----------------------------------------------------------------

camera.Operations.open()
is_open = camera.Status.is_open()
print(f'camera is open:{is_open}')

camera.Operations.start_grabbing()
is_grabbing = camera.Status.is_grabbing()
print(f'camera is grabbing:{is_grabbing}')

trigg_status = camera.Status.is_trigger_on()
print(f'trigger:{trigg_status}')

