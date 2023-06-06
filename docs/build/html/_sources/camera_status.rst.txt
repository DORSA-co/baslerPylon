Camera Status
==============================

Status Class
----------------------------
In ``Status`` atribiute of ``Camera`` class you can access to the status of the camera such as whether the camera is open or not.
This section also shows the structural parameters of the camera such as temperature



lets see some exmaples. in first step lets connect to the first camera
.. code-block:: python

   import dorsaPylon
   from dorsaPylon import Collector

   collector = Collector()
   camera = collector.get_all_cameras(camera_class=None)[0]


**exmaple1: check is camera open**
the ``is_open`` methode return `True` if camera is open.  O.w return ``False``

.. code-block:: python

   #lets open the camera
   camera.Operations.open()

   #check camera is open
   is_open = camera.Status.is_open()

   if is_open:
      print(f'camera is open')
   else:
      print(f'camera is close')
   
.. code-block::

   $ camera is open


**exmaple2: check is camera open**
the ``is_grabbing`` methode return ``True`` if camera is grabbing. O.w return ``False``

.. code-block:: python

   #start grabbing camera
   camera.Operations.start_grabbing()

   #check camera is grabbing
   is_grabbing = camera.Status.is_grabbing()

   if is_grabbing:
      print(f'camera is grabbing')
   else:
      print(f'camera is stop')

   
.. code-block::

   $ camera is stop






camera temperature
^^^^^^^^^^^^^^^^^^^^^
the ``get_tempreture`` methode return temperature of camera in ``float`` type

.. code-block:: python

   #get camera temperature
   temp = camera.Status.get_tempreture()

   print(f'temperature is {temp}')

   
.. code-block::

   $ temperature is 50.0






more sources
------------------
for more information see  
:doc:`Camera_src`

