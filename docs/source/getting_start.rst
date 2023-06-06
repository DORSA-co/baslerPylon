Getting start
===================

step 1: get Cameras
^^^^^^^^^^^^^^^^^^^^^^^^^^
You can manage cameras using Collector class . Use ``get_all_cameras`` function to get all connected cameras.
for more information see chapter :doc:`manageـdeviceـbyـCollector`

.. code-block:: python

   import dorsaPylon
   from dorsaPylon import Collector

   collector = Collector()

   #-----------------------------------------------------------------
   #get all avialble cameras 
   all_cameras = collector.get_all_cameras(camera_class=None)


Step 2: get picture
^^^^^^^^^^^^^^^^^^^^^^^^^^
In the next step, we take a picture from the first camera using the ``getPictures`` method


.. code-block:: python

   camera1 = all_cameras[0]
   
   #you should start grabbing befor call getPictures function
   camera1.camera.Operations.start_grabbing()

   #capture image from camera
   img = camera1.getPictures()

   cv2.imshow('img', img)
   cv2.waitKey(0)



Adjust camera parameters
^^^^^^^^^^^^^^^^^^^^^^^^^^
You can adjust all camera parameters like gain using  ``set_****`` functions of ``.Parms`` atribiute. Consider the example below

.. code-block:: python

   #set gain parameter 250
   camera1.Parms.set_gain(250)

   #read gain value from camera
   gain = camera1.Parms.get_gain()

   print(f'gain is {gain}')


.. code-block:: 

   $ gain is 250


change camera colorspace
^^^^^^^^^^^^^^^^^^^^^^^^^^
If you need to change the colorspace of the camera's images, for example when you work with mono color cameras,
you can change the camera pixelType using the ``build_converter`` function. For convenience, you can use the built-in flags in the ``PixelType`` class for the function argument.

.. code-block:: python
   
   #set pixeltype of camera gray 8bit
   camera1.build_converter(pixel_type=dorsaPylon.PixelType.GRAY8)
   gray_img = camera1.getPictures()

   #set pixeltype of camera gray 8bit
   camera1.build_converter(pixel_type=dorsaPylon.PixelType.BGR8)
   bgr_img = camera1.getPictures()

   print('gray image shape is', gray_img.shape)
   print('bgr image shape is', bgr_img.shape)

.. code-block:: 

   $ gray image shape is (1200,1920)
   $ bgr image shape is (1200,1920,3)




more advanced
^^^^^^^^^^^^^^^^^^^^^^^^^^
If you need to access the directly to official pypylon camera object, you can use ``camera_device`` attribute of ``Camera`` class

.. code-block:: python
   
   pypylon_camera_object = camera1.camera_device
   
   serial_number = pypylon_camera_object.camera_device.DeviceInfo.GetSerialNumber()
   
