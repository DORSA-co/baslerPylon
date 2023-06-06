# Steup
◌Instructions:<br />
  &emsp;1-pip install pypylon <br />
  &emsp;2-clone repository <br />

# Documention 
 To view the documents, first clone the project and then go to `docs/build/html` folder and open `index.html`.

# Step1: Get Devices And Camera
you can get cameras in two ways, by the `get_all_cameras` function or `get_camera_by_serial` .
the `get_all_cameras` function, return list of available cameras in your ideal camera class like GigE, USB and etc. If pass `camera_class` argument None, it returns all cameras in different classes
``` python
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
```
# Camera Functions
## Infoes
`Infoes` attribute is used for showing all camera information like serial number and model
``` python
model = camera.Infos.get_model()
print(f'model: {model}')

serial = camera.Infos.get_serialnumber()
print(f'serial: {serial}')

is_gige = camera.Infos.is_GigE()
print(f'is camera GigE: {is_gige}')
```
results:
```
>> model: Emulation
>> serial: 0815-0000
>> is camera GigE: False
```
## Parms
The `Parms` attribute is used to set all camera parameters like gain and exposure. you can also use this attribute to read parameters from the camera
``` python
#-----------------------------------------------------------------
#Parms is useing for set camera options
camera.Parms.set_gain(50)
gain = camera.Parms.get_gain()
print(f'gain is {gain}')

camera.Parms.set_trigger_on()
trigger = camera.Parms.get_trigger_mode()
print(f'trgigger is {trigger}')
#----------------------------------------------------------------
```
results:
```
>> GainRaw should be in range 192 up to 1023  in this device
>> gain is 192
>> trgigger is On
```
for some features, you can use `availble_xxxx` methods to get all possible values that you can set for that specific value

``` python
possible_triggerselector_value = camera.Parms.availble_triggerselector_values()
print(f'possible trigger selector value is:{possible_triggerselector_value}')
```
result:
```
possible trigger selector value is:('AcquisitionStart',)
```

## Status
The `status` attribute is used to get the status of the camera like camera grabbing status or is camera open or not and also stuff like camera temperature
``` python
camera.Operations.open()
is_open = camera.Status.is_open()
print(f'camera is open:{is_open}')

camera.Operations.start_grabbing()
is_grabbing = camera.Status.is_grabbing()
print(f'camera is grabbing:{is_grabbing}')

trigg_status = camera.Status.is_trigger_on()
print(f'trigger:{trigg_status}')
```
results:
```
>> camera is open:True
>> camera is grabbing:True
```

# Grab Image
for grabbing images, you can easily use the `getPictures` method. if you need to change pixel type, for example when you using a mono camera, you can change pixel type by the `build_converter` function. see example

``` python
#define your ideal pixel_type, defualt is BGR8
camera.build_converter(pixel_type=dorsaPylon.PixelType.GRAY8)
#-----------------------------------------------------------------
img = camera.getPictures()
cv2.imshow('img', img)
cv2.waitKey(0)
```

# Camera Emulation
this library support camera emulation. To enable camera emulation you can use the `enable_camera_emulation` method in the `Collector` class. you should pass the number of cameras that you want into this method. after calling this method, camera emulation would be added to the list of devices

``` python 
collector = Collector()
#enable camera emulation and pass your ideal camera counts
collector.enable_camera_emulation(2)
#get avialble cameras in class of emlulation
cameras = collector.get_all_cameras(camera_class=dorsaPylon.CamersClass.emulation)
cam1 = cameras[0]
#-----------------------------------------------------------------
cam1.Parms.set_gain(50)
cam1.Operations.start_grabbing()
```
# others
## 1- search node
if you are using a specific camera and you need a custom feature, you can use the `search_in_nodes(*keywords)` method to find your desired feature( node ) in the camera. this function gets one or more keywords in the `str` type and returns all nodes in your camera that contain these keywords. 
in this example, we want to find all features of the camera that are related to the `gain` keyword.
``` python 
nodes_name = cam1.search_in_nodes('gain')
print(f'first nodes name is {nodes_name[0]}')
```
result:

```
>> first nodes name is GainRaw
```

now you can set a value to this node by its name. you can use the `set_node` method

``` python 
cam1.Parms.set_node('GainRaw', 195)
gain = cam1.Parms.get_node('GainRaw')
print(f'gain set {gain}')
```
resut:
```
>> gain set 195
```

if possible values for a node are predefined strings (e.g. 'On', 'Off' ), you can use the x method to get all possible values that could be set to the node
``` python 
node_name = 'ExposureMode'
possible_values = cam1.Parms.availble_node_values(node_name)
print(f'possible value for {node_name} is: {possible_values}')
```
result:
```
possible values for ExposureMode are: ('Timed',)
```



