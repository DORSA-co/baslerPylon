Manage cameras by Collector
==============================

Collector class
^^^^^^^^^^^^^^^^^
You can manage cameras using ``Collector`` class. So for the first step you need to create an instance of this class

.. code-block:: python

   import dorsaPylon
   from dorsaPylon import Collector

   collector = Collector()


get all Cameras
^^^^^^^^^^^^^^^^^^^^^^^^^^
Use ``get_all_cameras`` function to get all connected cameras. this functions return a list
of `Camera` objects

.. code-block:: python

   #get all avialble cameras 
   all_cameras = collector.get_all_cameras(camera_class=None)

   print(f'{len(all_cameras)} devices founded')

.. code-block:: 

   $ 2 devices founded




get all Cameras in specific class
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can also filter cameras by their class using the ``camera_class`` argument, such as Gige and USB. If set this argument ``None``, this function returns all cameras in different classes

.. code-block:: python

   #get all avialble cameras That Are GigE
   gige_cameras = collector.get_all_cameras(camera_class=dorsaPylon.CamersClass.gige)




get camera by its serial number
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
You can get a camera based on its serial number by using the A function

.. code-block:: python

   #Receive camera with serial number
   camera = collector.get_camera_by_serial('123456')

   #read serial number from camra
   serial = camera.Infos.get_serialnumber()

   print(f"camera's serial number is {camera}")

.. code-block:: 

   $ cameras serial number is 123456




more sources
------------------
:doc:`Collector_src`