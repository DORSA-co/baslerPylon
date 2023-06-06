Camera parameters
==============================

Parms Class
----------------------------
You can access to all parametes of camera (such as gain and exposure) using ``Parms`` atribiute of ``Camera`` class.
This attribute includes three main function categories:

*  ``set_****`` methods. These methods are used to set the value of a parameter
*  ``get_****`` methods. These methods are used to get the value of a parameter
*  ``availble_****`` methods. These methods return the allowed values for a parameter

.. note::
   If you set the parameter value outside the allowed limit, a warning will be printed and the value of that parameter will be set to the minimum or maximum value depending on the value you entered.

lets see some exmaples. in first step lets connect to the first camera
.. code-block:: python

   import dorsaPylon
   from dorsaPylon import Collector

   collector = Collector()
   camera = collector.get_all_cameras(camera_class=None)[0]


**exmaple1: gain**
in this example we set the gain of camera and read value from camera

.. code-block:: python

   #set the gain 50
   camera.Parms.set_gain(50)

   #read gain value from camera
   gain = camera.Parms.get_gain()

   print(f'gain is {gain}')

.. code-block::

   $ gain is 50


**exmaple2: exposure**
in this example we set the exposure of camera and read value from camera

.. code-block:: python

   #set the gain 50
   camera.Parms.set_exposureTime(2000)

   #read gain value from camera
   exposure = camera.Parms.get_exposureTime()

   print(f'exposure is {exposure}')

.. code-block::

   $ exposure is 2000


**exmaple3: trigger**
lets work with camera trigger options

.. code-block:: python
   
   #turn On trigger
   camera.Parms.set_trigger_on()
   
   #get trigger mode is 'On' or 'Off'
   trigger_mode = camera.Parms.get_trigger_mode()
   
   print(f'trgigger is {trigger_mode}')

.. code-block::

   $ trgigger is On

now lets see avialble values for trgigger source of your camera
.. code-block:: python
   
   #get possible value that can be set fot trigger selector
   possible_triggersource_value = camera.Parms.availble_triggersource_values()

   print(f'possible trigger source values are:{possible_triggersource_value}')

.. code-block::

   $ possible trigger source values are:('Software',)

now setup trigger options

.. code-block:: python
   
   #set trigger source software
   #trigger selector value defualt is frame_start
   camera.Parms.set_trigger_option(dorsaPylon.Trigger.source.software,
                                dorsaPylon.Trigger.selector.frame_start
                                )



Advanced: specific nodes
----------------------------
Some cameras have features that may not be included in this library. In this section, we are going to explain how to set these parameters or actually nodes

set custom node
^^^^^^^^^^^^^^^^^^^^^^
To set a custom parameter, you need to know its node name. If you do not know the name of the parameter on your camera, you can use the search tool in the next section

You can set the value of a parameter using the ``set_node`` method of ``Parms`` class .
This function receives two inputs. The first argument is the name of the parameter or node and the second argument is the desired value for that parameter.

lets see example

.. code-block:: python
   
   camera.Parms.set_node('GainRaw', 195)


You also can get the value of a parameter using the ``get_node`` method of ``Parms`` class.
This function receives node's name as argument and return value of node

lets see example

.. code-block:: python
   
   gain = cam1.Parms.get_node('GainRaw')
   print(f'gain is {gain}')

.. code-block::

   $ gain is 195


If the value of the parameter is set with predefined strings, such as exposureMode, which takes two values, ``On`` and ``off``,
You can get the allowed values using the method ``availble_node_values`` method of ``Parms`` class.
This function receives node's name as argument and return a list of possible value for that node


.. code-block:: python
   
   node_name = 'ExposureMode'

   #get possible value for node ExposureMode
   possible_values = camera.Parms.availble_node_values(node_name)

   print(f'possible value for {node_name} is: {possible_values}')

.. code-block:: 

   $ possible values for ExposureMode are: ('Timed',)

search node
^^^^^^^^^^^^^^^^^^^^^^
If you need to set a node but don't know its exact name, you can use the ``search_in_nodes(*keywords)`` method to find your desired feature( node ) in your specific camera.
this function gets one or more keywords in the ``str`` type and returns all nodes in your camera that contain these keywords.

in this example, we want to find all features of the camera that are related to the ``gain`` keyword.

.. code-block:: python
   
   nodes_name = cam1.search_in_nodes('gain')

   print(f'{len(nodes_name)} nodes founded')
   print(f'first nodes name is {nodes_name[0]}')

.. code-block::

   $ 3 nodes founded
   $ first nodes name is GainRaw



more sources
------------------
for more information see  
:doc:`Camera_src`

