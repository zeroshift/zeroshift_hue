zeroshift_hue
=============

My hue module for Python. Trying to match the official API.

Example:

.. code-block:: python

    from zeroshift_hue import Hue

    h = Hue(devicetype="zeroshift_hue") #username="username" if you already have one
    username = h.authenticate() #Save the username if you're generating one now

    lights = getAllLightObjects()

    for light in lights:
        light.blinkRed()
