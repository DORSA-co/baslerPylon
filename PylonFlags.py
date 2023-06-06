from pypylon import pylon

class CamersClass:
    gige = "BaslerGigE"
    usb = "BaslerUSB"
    emulation = 'BaslerCamEmu'


#-------------------------------------
class TrigggerSource:
    software = 'Software'
    hardware_line1 = 'Line1'

class TriggerSelector:
    frame_start = 'FrameStart'

class Trigger:
    source = TrigggerSource    
    selector = TriggerSelector
#-------------------------------------

class PixelType:
    RGB8 = pylon.PixelType_RGB8packed
    BGR8 = pylon.PixelType_BGR8packed
    GRAY8 = pylon.PixelType_Mono8


class GrabStrategy:
    last_image = pylon.GrabStrategy_LatestImageOnly
    onebyone = pylon.GrabStrategy_OneByOne