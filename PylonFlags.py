from pypylon import pylon

class GetPictureErrors:
    no_error = 0
    is_not_open = 1
    is_not_grabbing = 2
    phisically_remove = 3
    buffer_empty = 4
    grabresult_error = 5




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
    GRAY10 = pylon.PixelType_Mono10


class GrabStrategy:
    latest_image = pylon.GrabStrategy_LatestImageOnly
    #last_image_only = pylon.GrabStrategy_LatestImages
    onebyone = pylon.GrabStrategy_OneByOne
    upcoming_image = pylon.GrabStrategy_UpcomingImage


class GammaMode:
    user = 'User'
    srgb = 'sRGB'


class Color:
    Red = 'Red'
    Green = 'Green'
    Blue = 'Blue'

class LightSource:
    Daylight6500K = 'Daylight6500K'