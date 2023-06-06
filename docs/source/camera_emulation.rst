Camera Emulation
==============================

Introduction
^^^^^^^^^^^^^^^^^^
camera emulation is a virtual camera which supports some of the features of the real camera.
This feature will be useful when you don't have access to a real camera during software development


Setup Camera emulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^
To enable camera emulation you can use the ``enable_camera_emulation method`` method in the ``Collector`` class.
you should pass the number of cameras that you want into this method. after calling this method, camera emulation would be added to the list of devices


.. code-block:: python

   import dorsaPylon
   from dorsaPylon import Collector

   collector = Collector()

   #enable camera emulation and pass your ideal camera counts
   collector.enable_camera_emulation(2)

   #get avialble cameras only in class of emlulation
   cameras = collector.get_all_cameras(camera_class=dorsaPylon.CamersClass.emulation)

   camera1 = cameras[0]
   
   #Set gain parameter
   camera1.Parms.set_gain(50)

