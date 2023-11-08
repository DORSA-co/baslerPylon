"""
########################################
---------------------------------------

Made with Malek & Milad

Features:

    ● Create Unlimite Object of Cameras and Live Preview By serial number
    ● Set Bandwitdh Of each Cameras
    ● Set gain,exposure,width,height,offet_x,offset_y
    ● Get tempreture of Cmeras
    ● Set Trigger Mode on
    ● There are Some diffrents between ace2(pro) and ace

---------------------------------------
########################################
"""
from pypylon import pylon
from PylonFlags import CamersClass, Trigger, PixelType
import cv2
import time
import numpy as np
import threading
import os
from pypylon import genicam
'''
                         !تذکر
از قرار دادن هرگونه اسد و پرینت اروووررررر جدا خودداری فرمایید
            حتی شما مدیر پروژه عزیز اکسین
'''
# 



'''
bandwidth manager
USB camera
offset_x , offset_y
'''

DEBUG = False
show_eror = False


class ErrorAndWarnings:
    @staticmethod
    def no_devices():
        return "ERROR: No Devices founded"

    @staticmethod
    def not_in_range(name, min_v, max_v):
        return f"{name} should be in range {min_v} up to {max_v}  in this device"
    
    @staticmethod
    def grab_error(error_code, error_description):
        return f'ERROR: error {error_code} happend! {error_description}'
    
    @staticmethod
    def error_code(error_code):
        return f'ERROR: error {error_code} happend!'

    @staticmethod    
    def value_not_available(name, availbles):
        return f"ERROR: only {availbles} could set for {name} in this device"
    
    @staticmethod
    def reset():
        return f"WARNING: camera reset! you should creat Camera Object again !!"
    
    @staticmethod
    def not_grabbing():
        return "ERROR: camera isn't grabbing. Start Grabbing First!"

    @staticmethod
    def node_not_avaiable():
        return 'predefine node not available, please set node by its name'
    











# class CameraOption:
#     def __init__(self, camera_device):
#         self.camera_device = camera_device







class Camera:
    """_summary_
    """
    def __init__(self, camera_device: pylon.InstantCamera):
        """some"""
        self.camera_device = camera_device
        
        self.Infos = CameraInfo(self)
        self.Parms = CameraParms(self)
        self.Status = CameraStatus(self)
        self.Operations = CameraOperations(self)
        self.image_event_handler = CameraImageEventHandler(self)

        
        self.converter = self.build_converter(PixelType.BGR8)
        self.nodes_name = self.get_available_nodes()
        self.timeout = 5000
        self.image = None

    def get_available_nodes(self,):
        nodeMap = self.camera_device.GetNodeMap()
        nodes = nodeMap.GetNodes()
        return list(map(lambda x:x.Node.Name, nodes))


    def is_node_available(self, node_name):
        return node_name in self.nodes_name
    
    def reset(self,):
        """Reset all camera settings
        """
        self.camera_device.DeviceReset()
        print(ErrorAndWarnings.reset())
        
    def search_in_nodes(self, *keywords) -> list[str]:
        """search in camera nodes by one or more keywords to find your intended feature

        Returns:
            List[Str]: List of nodes name that contains keywords
        """
        res = []
        for node in self.camera_device.NodeMap.GetNodes():
            flag = True
            for keyword in keywords:
                if keyword not in node.Node.Name.lower():
                    flag = False
                    break
            if flag:
                #res.append([node.Node.Name,node])
                res.append(node.Node.Name)
                print(node.Node.Name)
        return res
    

    def build_converter(self, pixel_type):
        """build a converter to determine the pixel type like RGB or MONO8
        """
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pixel_type
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        self.converter = converter
        return converter

    


    def set_image_event(self, func):
        if self.Status.is_open():
            self.Operations.close()
        #self.Operations.start_grabbing()
        self.camera_device.GrabCameraEvents.SetValue(True) #enable event handler
        self.image_event_handler.set_func(func)
        self.camera_device.RegisterImageEventHandler(self.image_event_handler, pylon.RegistrationMode_Append, pylon.Cleanup_Delete)


    def software_trige_exec(self):
        """execute software trigger"""
        self.camera_device.TriggerSoftware()
    

    def build_zero_image(self):
        """return a zero image with the dimensions of the camera image"""
        _,_,h,w = self.Parms.get_roi()
        img = np.zeros((h, w, 3), dtype=np.uint8)
        return img

    

    def getPictures(self, grabResult = None, img_when_error='zero') -> np.ndarray:
        """return an image if camera caReturns an image if the camera has captured an image

        Args:
            grabResult (_type_, optional): grabResult of camera. generally used for event. Defaults to None.
            img_when_error (str, optional): determine what returns when the captured image got an error. Defaults to 'zero'.

        Returns:
            np.ndarray: captured image
        """
        res_img = None
        ret = False
        if self.Status.is_grabbing():
            #-------------------------------------------------------------
            if grabResult is None:
                if self.Status.is_grabbing():
                    grabResult = self.camera_device.RetrieveResult(self.timeout, pylon.TimeoutHandling_ThrowException)
                else:
                    print(ErrorAndWarnings.not_grabbing())
            #-------------------------------------------------------------
            if grabResult is not None and grabResult.GrabSucceeded():
                image = self.converter.Convert(grabResult)
                res_img = image.Array
                ret = True
            elif grabResult is not None:
                print( ErrorAndWarnings.grab_error(grabResult.ErrorCode, grabResult.ErrorDescription))
            else:
                print(ErrorAndWarnings.not_grabbing())
            #-------------------------------------------------------------
        if res_img is None:
            if img_when_error == 'zero':
                res_img = self.build_zero_image()

        self.image = res_img
        return ret, res_img
    

class CameraInfo:
    def __init__(self, camera_object: Camera):
        """information of camera"""
        self.camera_object = camera_object

    def get_model(self) -> str:
        """return model of camera in `Str` type"""
        return self.camera_object.camera_device.GetDeviceInfo().GetModelName()
    
    def get_serialnumber(self) -> str:
        """return serial number of camera in `Str` type"""
        return self.camera_object.camera_device.DeviceInfo.GetSerialNumber()
    
    def get_class(self) -> str:
        """return calas of camera in `Str` type like BaslerGigE and BaslerUSB"""
        return self.camera_object.camera_device.DeviceInfo.GetDeviceClass()

    def is_PRO(self,) -> bool:
         """return True if camera is Pro model"""
         return 'pro' in self.get_model().lower()
    
    def is_USB(self,) -> bool:
         """ return True if camera is USB class"""
         return self.camera_object.camera_device.IsUsb()
    
    def is_GigE(self,) -> bool :
         """ return True if camera is GigE class"""
         return self.camera_object.camera_device.IsGigE()




class CameraStatus:
    def __init__(self, camera_object: Camera):
        """determine status of camera like open and grabbing"""
        self.camera_object = camera_object

    def is_open(self) -> bool:
        """ return True if camera be open"""
        return self.camera_object.camera_device.IsOpen()
    
    def is_grabbing(self) -> bool:
        """ return True if camera is grabbing"""
        return self.camera_object.camera_device.IsGrabbing()
    
    def is_trigger_on(self,) -> bool:
        """ return True if trigger be On"""
        return self.camera_object.Parms.__get_value__(self.camera_object.camera_device.TriggerMode).lower() == 'on'
    
    def get_tempreture(self) -> float:
        """return device tempreture

        Returns:
            float: device tempreture
        """
        if self.camera_object.is_node_available('DeviceTemperature'):
            return self.camera_object.camera_device.DeviceTemperature.GetValue()
        elif self.camera_object.is_node_available('TemperatureAbs'):
            return self.camera_object.camera_device.TemperatureAbs.GetValue()
        


class CameraOperations:
    def __init__(self, camera_object: Camera):
        """Perform operations on the camera"""
        self.camera_object = camera_object

    def open(self):
        """Open camera"""
        if not self.camera_object.Status.is_open():
            self.camera_object.camera_device.Open()
    
    def close(self):
        """close camera"""
        if self.camera_object.Status.is_open():
            self.camera_object.camera_device.Close()

    def start_grabbing(self, strategy = pylon.GrabStrategy_LatestImageOnly ):
        """start grabbing. it is necessary for capture image.
        - If the camera is not open, this function will do it automatically

        Args:
            strategy (_type_, optional): strategy of grabbing image. Defaults to pylon.GrabStrategy_LatestImageOnly.
        """
        self.open()
        if not self.camera_object.Status.is_grabbing():
            self.camera_object.camera_device.StartGrabbing(strategy)
    
    def stop_grabbing(self):
        """stop grabbing"""
        if self.camera_object.Status.is_grabbing():
            self.camera_object.camera_device.StopGrabbing()



class CameraParms:
    def __init__(self, camera_object: Camera):
        self.camera_object = camera_object

    

    def __set_value__(self, value, parameter):
        if not self.camera_object.Status.is_open():
            self.camera_object.Operations.open()
        
        if value is not None:
            if type(value) == int or type(value) == float:
                max_v = parameter.Max
                min_v = parameter.Min
                if not(min_v <= value <= max_v):
                    value = min(max(value, min_v), max_v)
                    print(ErrorAndWarnings.not_in_range(parameter.Node.Name, min_v, max_v))
            elif type(value) == str:
                if value not in self.__get_available_value__(parameter):
                    print(ErrorAndWarnings.value_not_available(parameter.Node.Name , self.__get_available_value__(parameter)))
                    return

            parameter.SetValue(value)

    
    def __get_value__(self, parameter):
        if not self.camera_object.Status.is_open():
            self.camera_object.Operations.open()
        return parameter.Value
    
    def __get_available_value__(self, parameter):
        return parameter.Symbolics

    def __get_value_range__(self, parameter):
        #        print(parameter.Node.Name, )
        access = parameter.Node.GetAccessMode()
        if access == 1:
            if not self.camera_object.Status.is_open():
                self.camera_object.Operations.open()
        max_v = parameter.Max
        min_v = parameter.Min
        return min_v, max_v

    


    def set_all_parms(
                        self,
                        gain=None,
                        exposure=None,
                        width=None,
                        height=None,
                        offset_x=None,
                        offset_y=None,
                        trigger=None,
                        trigge_source=None,
                        trigge_selector = None
                        ):
        """Set commonly used parameters at once
        ** If any parameter is set to `None`, that parameter will not be set on the camera 
        """
        
        self.set_gain(gain)
        self.set_exposureTime(exposure)
        self.set_trigger_option(trigge_source, trigge_selector)
        self.set_roi(height, width, offset_x, offset_y )
        if trigger:
            self.set_trigger_on()
        else:
            self.set_trigger_off()
        #self.max_buffer = max_buffer
        #self.cont_eror = 0
        #self.trigger = trigger
        #self.dp = delay_packet
        #self.ps = packet_size
        #self.ftd = frame_transmission_delay
        #self.exitCode = 0
        self.set_node()
    def set_node(self, node_name:str, value ):
        """set value to specefic node by its name
        Examples: 
            >>> camera.Parms.set_node('GainRaw', 230)

        Args:
            node_name (str): node name. you can find it by search in camera nodes using 
            ```Camera.search_in_nodes ``` method 
            value (_type_):
        """
        node = self.camera_object.camera_device.NodeMap.GetNode(node_name)
        self.__set_value__(value, node)
    
    def get_node(self, node_name: str ):
        """get value of specefic node by its name
        Examples: 
            >>> camera.Parms.get_node('GainRaw')
            >>> 230
        Args:
            node_name (str): node name. you can find it by search in camera nodes using 
            ```Camera.search_in_nodes ``` method 

        Returns:
            _type_: value of node
        """
        node = self.camera_object.camera_device.NodeMap.GetNode(node_name)
        return self.__get_value__(node)
    
    def availble_node_values(self, node_name:str):
        """returns list of available values for specific node by its name
        Examples: 
            >>> camera.Parms.availble_node_values('ExposureMode')
            >>> ('Timed',)

        Args:
            node_name (str): node name. you can find it by search in camera nodes using 
            ```Camera.search_in_nodes ``` method 
        Returns:
            _type_: _description_
        """
        node = self.camera_object.camera_device.NodeMap.GetNode(node_name)
        return self.__get_available_value__(node)

    def get_node_range(self, node_name:str) -> tuple:
        """returns range of allowable values for specific numberical node by its name
        Examples: 
            >>> camera.Parms.allowable('gainRaw')
            >>> (0, 200)

        Args:
            node_name (str): node name. you can find it by search in camera nodes using 
            ```Camera.search_in_nodes ``` method 
        Returns:
            tuple: (low, high) range
        """
        node = self.camera_object.camera_device.NodeMap.GetNode(node_name)
        return self.__get_value_range__(node)


    def set_gain(self, gain: int) -> None:
        """set gain of camera"""
        if self.camera_object.is_node_available('Gain'):
            self.__set_value__(gain, self.camera_object.camera_device.Gain)
        elif self.camera_object.is_node_available('GainRaw'):
            self.__set_value__(gain, self.camera_object.camera_device.GainRaw)
        else:
            print(ErrorAndWarnings.node_not_avaiable())
    
    def get_gain(self) -> int:
        """get gain of camera"""
        if self.camera_object.is_node_available('Gain'):
            return self.__get_value__( self.camera_object.camera_device.Gain)
        elif self.camera_object.is_node_available('GainRaw'):
            return self.__get_value__( self.camera_object.camera_device.GainRaw)
        else:
            print(ErrorAndWarnings.node_not_avaiable())

    def get_gain_range(self) -> tuple[int, int]:
        """get allowable range of gain of camera"""
        if self.camera_object.is_node_available('Gain'):
            return self.__get_value_range__( self.camera_object.camera_device.Gain)
        elif self.camera_object.is_node_available('GainRaw'):
            return self.__get_value_range__( self.camera_object.camera_device.GainRaw)
        else:
            print(ErrorAndWarnings.node_not_avaiable())


    def set_exposureTime(self, exposure: int) -> None:
        """set ExposureTime of camera"""
        if self.camera_object.is_node_available('ExposureTime'):
            self.__set_value__(exposure, self.camera_object.camera_device.ExposureTime)

        elif self.camera_object.is_node_available('ExposureTimeAbs'):
            self.__set_value__(exposure, self.camera_object.camera_device.ExposureTimeAbs)

        else:
            print(ErrorAndWarnings.node_not_avaiable())
    
    def get_exposureTime(self) -> int:
        """get ExposureTime of camera"""
        if self.camera_object.is_node_available('ExposureTime'):
            return self.__get_value__( self.camera_object.camera_device.ExposureTime)
        
        elif self.camera_object.is_node_available('ExposureTimeAbs'):
            return self.__get_value__(self.camera_object.camera_device.ExposureTimeAbs)
        
        else:
            print(ErrorAndWarnings.node_not_avaiable())
            

    def get_exposureTime_range(self) -> tuple [int, int]:
        """get allowable range of ExposureTime of camera"""
        if self.camera_object.is_node_available('ExposureTime'):
            return self.__get_value_range__( self.camera_object.camera_device.ExposureTime)
        
        elif self.camera_object.is_node_available('ExposureTimeAbs'):
            return self.__get_value_range__(self.camera_object.camera_device.ExposureTimeAbs)
        
        else:
            print(ErrorAndWarnings.node_not_avaiable())


    def set_roi(self, height: int, width: int, offset_x: int, offset_y: int) -> None:
        """set roi of camera

        Args:
            height (int): height of camera
            width (int): width of camera
            offset_x (int): 
            offset_y (int):
        """
        grabbing = False
        if self.camera_object.Status.is_grabbing():
            self.camera_object.Operations.stop_grabbing()
            grabbing = True
        self.__set_value__(width, self.camera_object.camera_device.Width)
        self.__set_value__(height, self.camera_object.camera_device.Height)
        self.__set_value__(offset_x, self.camera_object.camera_device.OffsetX)
        self.__set_value__(offset_y, self.camera_object.camera_device.OffsetY)

        if grabbing:
            self.camera_object.Operations.start_grabbing()

    
    def get_roi(self,) -> tuple[ int, int, int, int]:
        """return roi parameters of camera

        Returns:
            tuple[ int, int, int, int]: h, w, offset_x, offset_y
        """
        w = self.__get_value__( self.camera_object.camera_device.Width)
        h = self.__get_value__( self.camera_object.camera_device.Height)
        offset_x = self.__get_value__( self.camera_object.camera_device.OffsetX)
        offset_y = self.__get_value__( self.camera_object.camera_device.OffsetY)
        return h, w, offset_x, offset_y


    def get_roi_range(self,) -> tuple[ tuple, tuple, tuple, tuple]:
        """return allowable range of roi parameters of camera

        Returns:
            tuple[ tuple, tuple, tuple, tuple]: __get_value_range__
        """
        w_range = self.__get_value_range__( self.camera_object.camera_device.Width)
        h_range = self.__get_value_range__( self.camera_object.camera_device.Height)
        offset_x_range = self.__get_value_range__( self.camera_object.camera_device.OffsetX)
        offset_y_range = self.__get_value_range__( self.camera_object.camera_device.OffsetY)
        return h_range, w_range, offset_x_range, offset_y_range 
    
    def set_trigger_option(self, source: str, selector = Trigger.selector.frame_start) -> None:
        """setup trigger option ( trigger source and trigger selector) 
        Examples:
            >>> camera.Parms.set_trigger_option(Trigger.source.software, Trigger.selector.frame_start)


        Args:
            source (str): source of trigger 
                Trigger.source.software
                Trigger.hardware_line1

            selector (_type_, optional): trigger selector. Defaults to Trigger.selector.frame_start.
        """
        self.set_trigger_on()
        self.__set_value__(source, self.camera_object.camera_device.TriggerSource)
        self.__set_value__(selector, self.camera_object.camera_device.TriggerSelector)

    def get_trigger_option(self) -> tuple[str, str]:
        """return values of TriggerSource and TriggerSelector

        Returns:
            tuple[str, str]: source, selector
        """
        source = self.__get_value__(self.camera_object.camera_device.TriggerSource)
        selector = self.__get_value__(self.camera_object.camera_device.TriggerSelector)
        return source, selector
    
    
    def availble_triggersource_values(self) -> tuple[str]:
        """return avaible value for TriggerSource node of camera

        Returns:
            tuple[str]: avaible value for TriggerSource node of camera
        """
        return self.__get_available_value__(self.camera_object.camera_device.TriggerSource)
    
    def availble_triggerselector_values(self) -> tuple[str]:
        """return avaible value for TriggerSelector node of camera

        Returns:
            tuple[str]: avaible value for TriggerSelector node of camera
        """
        return self.__get_available_value__(self.camera_object.camera_device.TriggerSelector)


    def set_trigger_on(self) -> None:
        """trun trigger `On` """
        self.__set_value__('On', self.camera_object.camera_device.TriggerMode)
        

    def set_trigger_off(self) -> None:
        """trun trigger `Off` """
        self.__set_value__('Off', self.camera_object.camera_device.TriggerMode)

    def get_trigger_mode(self) -> str:
        """return trigger mode value (`On` or `Off`)"""
        return self.__get_value__(self.camera_object.camera_device.TriggerMode)

    def set_bandwith(self,):
        #fps = bandwidth / payload_size
        pass

    def set_transportlayer(self,packet_delay: int, packet_size = None) -> None:
        """set packet_delay and packet_size of camera

        Args:
            packet_delay (int):
            packet_size (int, optional): Defaults to None.
        """
        self.__set_value__(packet_size, self.camera_object.camera_device.GevSCPSPacketSize)
        self.__set_value__(packet_delay, self.camera_object.camera_device.GevSCPD)



class CameraImageEventHandler(pylon.ImageEventHandler):
    def __init__(self,camera : Camera, *args):
        super().__init__(*args)
        self.event_func = None
        self.camera = camera

    def set_func(self, func):
        self.event_func = func

    def OnImageGrabbed(self, camera, grabResult):
        print("CameraImageEventHandler.OnImageGrabbed called.")
        img = self.camera.getPictures(grabResult)
        if self.event_func is not None:
            self.event_func(img)










class Collector:
    def __init__(
        self,
        camera_class = None,
    ):
        """modify devices camera

        Args:
            camera_class (_type_, optional): _description_. Defaults to None.
        """
        self.camera_class = camera_class

        self.__tl_factory = pylon.TlFactory.GetInstance()
        # ----------------------------------------------------------
        self.devices = self.get_available_devices(self.camera_class)
        self.cameras = None
        #assert self.devices, ErrorAndWarnings.no_devices()
        # ----------------------------------------------------------
    def enable_camera_emulation(self, count:int):
        """enable camera emulation device for testing and developing purpose

        Args:
            count (int): number of emulation device
        """
        os.environ['PYLON_CAMEMU'] = str(count)

    def get_available_devices(self, camera_class=None) -> list[Camera]:
        """return list of available devices
        Examples:
            return all gige devices
            >>> founded = collector.get_available_devices(CamersClass.gige)
        Args:
            camera_class (_type_, optional): filter devices by camera class like Gige or USB.
            - it could be CamersClass.*
            - if be None, return all devices in diffrents class. Defaults to None.
        

        Returns:
            List[pyplone.device]: list of devices in determined class
        """
        founded_devices = []
        for device in self.__tl_factory.EnumerateDevices():
            if device.GetDeviceClass() == camera_class or camera_class is None:
                founded_devices.append(device)
        return founded_devices
    
    def listDevices(self):
        """print information of available devices"""
        cameras = self.get_all_cameras()
        for i, camera in enumerate(cameras):
            device_info = camera.GetDeviceInfo()
            print(
                "Camera #%d %s @ %s (%s) @ %s"
                % (
                    i,
                    device_info.GetModelName(),
                    device_info.GetIpAddress(),
                    device_info.GetMacAddress(),
                    device_info.GetSerialNumber(),
                )
            )


    def get_camera_by_serial(self, serial_number:str) -> Camera:
        """get a camera by its serial number

        Args:
            serial_number (str): serial number of camera

        Returns:
            Camera: 
        """
        self.devices = self.get_available_devices(None)
        for device in self.devices:
            camera = pylon.InstantCamera(self.__tl_factory.CreateDevice(device))
            if camera.GetDeviceInfo().GetSerialNumber() == serial_number:
                return Camera(camera)
        return None

    def get_all_cameras(self, camera_class=None) -> list[Camera]:
        """return list of available devices

        Examples:
            >>> cameras = collector.get_all_cameras(CamersClass.gige)

        Args:
            camera_class (_type_, optional): filter devices by camera class like Gige or USB.
            - you can use CamersClass.* flags
            - if be None, return all cameras in diffrents class. Defaults to None.

        Returns:
            List[Camera]: list of cameras in determined class
        """
        self.devices = self.get_available_devices(None)
        cameras = []
        for device in self.devices:
            if camera_class is None or device.GetDeviceClass() == camera_class:
                cameras.append(
                    Camera(pylon.InstantCamera(self.__tl_factory.CreateDevice(device)))
                )

        return cameras
        

    
    def get_all_serials(self,) -> list[str]:
        """return list of serialnumber of available cameras"""
        self.devices = self.get_available_devices(None)
        serial_list = []
        for device in self.devices:
            sn = device.GetSerialNumber()
            serial_list.append(sn)
        return serial_list


# eMyExposureEndEvent = 100
# class SampleCameraEventHandler(pylon.CameraEventHandler):
#     # Only very short processing tasks should be performed by this method. Otherwise, the event notification will block the
#     # processing of images.
#     def OnCameraEvent(self, camera, userProvidedId, node):
#         print('ffffffffffffffff')
#         if userProvidedId == eMyExposureEndEvent:
#             print("Exposure End event. FrameID: ", camera.EventExposureEndFrameID.Value, " Timestamp: ",
#                   camera.EventExposureEndTimestamp.Value)
#             # More events can be added here.


# def test_event(img):
#     print('tesssssssssst')

# handler1 = SampleCameraEventHandler()



# if __name__ == "__main__":
#     time.sleep(1)
#     collector = Collector()
#     collector.enable_camera_emulation(2)
#     cameras = collector.get_all_cameras(camera_class=CamersClass.emulation)
#     cam1 = cameras[0]
#     #-----------------------------------------------------------------
#     cam1.Parms.set_gain(50000)
#     cam1.Operations.start_grabbing()
#     cam1.search_in_nodes('gain')
#     #cam1.set_image_event(func=test_event)
    
#     #-----------------------------------------------------------------
#     cam1.Parms.set_gain(0)
#     # cam1.set_image_event(test_event)
#     # cam1.Operations.start_grabbing()
#     # cam1.software_trige_exec()
#     # cam1.getPictures()
#     # cam1.camera_device.EventSelector.SetValue('ExposureEnd')
    

#     #-----------------------------------------------------------------------
#     #cam1.Operations.close()
#     # cam1.camera_device.RegisterConfiguration(pylon.SoftwareTriggerConfiguration(), pylon.RegistrationMode_ReplaceAll,
#     #                              pylon.Cleanup_Delete)
    
#     # cam1.camera_device.GrabCameraEvents.SetValue(True) #enable event handler
#     # cam1.camera_device.RegisterCameraEventHandler(handler1, "ExposureEndEventData", eMyExposureEndEvent, pylon.RegistrationMode_ReplaceAll, pylon.Cleanup_None)

#     # cam1.Operations.open()

#     # cam1.camera_device.EventSelector.SetValue('ExposureEnd')
#     # cam1.camera_device.EventNotification.SetValue('On')
#     #-----------------------------------------------------------------------

#     #cam1.Parms.set_trigger_option(Trigger.source.software, Trigger.selector.frame_start)
#     cam1.Operations.start_grabbing()
#     # 

#     # cam1.Operations.open()
#     # cam1.Operations.start_grabbing()
    
    
#     #i  = cam1.getPictures()
#     cam1.software_trige_exec()
#     while True:
        
#         cam1.software_trige_exec()
#         time.sleep(0.2)
#         cam1.getPictures()
#     pass
#     #a = pylon.InstantCamera()
#     #x = pylon.InstantCamera()
