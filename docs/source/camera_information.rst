Access camera information
==============================

Infos Class
^^^^^^^^^^^^^^^^^
You can access to all information of camera using ``Info`` atribiute of ``Camera`` class. This attribute manages the parameters of the camera that are inherent such as camera-model and serial-number.
In the example below, we use the ``get_serialnumber`` method to get the camera model

.. code-block:: python

   import dorsaPylon
   from dorsaPylon import Collector, Camera

   #get first camera
   collector = Collector()
   camera = collector.get_all_cameras(camera_class = None)[0]
   
   #get model of camera
   model = camera.Infos.get_model()

   print(f'model: {model}')

.. code-block:: 

   $ model: acA1920-40gm


Now let's get the camera class and its serial number as well

.. code-block:: python

   #get serial numbr of camera
   sn = camera.Infos.get_serialnumber()

   #get class of camera ( gige, usb, cameralink,... )
   cc = camera.Info.get_class()

   print(f'serial number: {sn}')
   print(f'camera class: {cc}')

.. code-block:: 

   $ serial number: 386313863
   $ camera class: BaslerGigE


check camera class and type
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
For more convenience, you can use the functions like ``is_USB``, ``is_GigE``, ``is_PRO``` and so on. this functions return ``bool``

.. code-block:: python

   #return True if camera is GigE
   is_gige = camera.Infos.is_GigE()

   #return True if camera is Pro model
   is_pro = camera.Infos.is_PRO()

   print(f'is camera GigE: {is_gige}')
   print(f'is camera Pro: {is_pro}')

.. code-block:: 

   $ is camera GigE: True
   $ is camera Pro: False



more sources
------------------
for more information see  
:doc:`Camera_src`