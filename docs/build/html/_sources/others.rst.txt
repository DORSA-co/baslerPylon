others atribiute
==============================

build_zero_image
----------------------------
``build_zero_image`` method of ``Camera`` returns a zero image the same size as the camera image

.. code-block:: python

   img = camera.build_zero_image()


build_converter
--------------------------
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





more sources
------------------
for more information see  
:doc:`Camera_src`

