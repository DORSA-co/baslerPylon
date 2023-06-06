Camera Operations
==============================

Operations Class
----------------------------
``Operations`` atribiute of ``Camera`` class handle camera operation such as Open camera and start_grabbing


lets see some exmaples. in first step lets connect to the first camera
.. code-block:: python

   import dorsaPylon
   from dorsaPylon import Collector

   collector = Collector()
   camera = collector.get_all_cameras(camera_class=None)[0]


**exmaple1: Open and start grabbing**
In the example below, we open the camera and start grabbing and close it after capture the image

.. code-block:: python

   #open the camera
   camera.Operations.open()
   
   #start grabbing image
   camera.Operations.start_grabbing()

   #capture image
   img = camera.getPictures()


   #close camera
   camera.Operations.close()



.. note::
   when you call ``start_grabbing`` method, it open camera automatically and don't need open camera before call ``start_grabbing``


.. note::
   As it is clear in the above example, the ``getPictures`` method is placed in class ``Camera`` directly, due to its high usage




more sources
------------------
for more information see  
:doc:`Camera_src`

