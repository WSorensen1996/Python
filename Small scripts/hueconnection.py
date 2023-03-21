from phue import Bridge
import time

bridge_ip_address = 'xx.x.x.xxx'

def access_lights(bridge_ip_address):
    b = Bridge(bridge_ip_address)
    light_names_list = b.get_light_objects('name')
    return light_names_list

def lights():
    lights = access_lights(bridge_ip_address)
    for light in lights:
        lights[light].on = True
        lights[light].hue = 1
        lights[light].saturation = 1

lights()

