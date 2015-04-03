#!/usr/bin/env python

import json
import requests
import sys, time
from threading import *
import logging

class Hue(object):
    def __init__(self, devicetype="zeroshift-hue", username=None, bridge_ip=None, debug=False):
        self.bridge_ip = bridge_ip
        if not self.bridge_ip:
          self.bridge_ip = self._getBridgeIP() 
        
        self.devicetype = devicetype
        self.username = username

    def authenticate(self):
        did_get_username = False
        if self.username:
            return True
        else:
            count = 0
            while count < 6:
                response = self._createUser(self.devicetype)
                if response[0].has_key('error'):
                    logging.warning("Warning: {0}".format(response[0]['error']['description']))
                elif response[0].has_key('success'):
                    self.username = response[0]['success']['username']
                    did_get_username = True
                    break
                else:
                    logging.error('Something went wrong.')
                count += 1
                time.sleep(5)
            return did_get_username

    def _getBridgeIP(self): 
        try:
            response = self._discoverLocalBridges()
            bridge_ip = response[0]['internalipaddress']
            logging.debug("Discovered bridge. IP: {0}".format(bridge_ip))
            return bridge_ip
        except:
            logging.debug("Could not get bridge IP!")
            return False

    # Custom
    def getLightObject(self, light_id):
        light = Light(self, light_id)
        return light

    def getAllLightObjects(self):
        lights = []
        for light_id in self._getAllLights():
            light = Light(self, light_id)
            lights.append(light)
        return lights

    def _getLightState(self, light_id):
        r = requests.get(("http://%s/api/%s/lights/%s" % (self.bridge_ip, self.username, light_id)))
        return json.loads(r.text)['state']

    def _setLightStateWithPayload(self, light_id, payload):
        r = requests.put(("http://%s/api/%s/lights/%s/state" % (self.bridge_ip, self.username, light_id)), json.dumps(payload))
        return json.loads(r.text)

    # Lights
    def _getAllLights(self):
        r = requests.get(("http://%s/api/%s/lights" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def _getNewLights(self):
        r = requests.get(("http://%s/api/%s/lights/new" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def _searchNewLights(self):
        r = requests.post(("http://%s/api/%s/lights" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def _getLightAttribsAndState(self, light_id):
        r = requests.get(("http://%s/api/%s/lights/%s" % (self.bridge_ip, self.username, light_id)))
        return json.loads(r.text)

    def _setLightName(self, light_id, name):
        payload = {'name': name}
        r = requests.put(("http://%s/api/%s/lights/%s" % (self.bridge_ip, self.username, light_id)), json.dumps(payload))
        return json.loads(r.text)

    def _setLightState(self, light_id, **kwargs):
        """ Required: light_id. Optional: on, bri, hue, sat, xy, ct, alert, effect, transiontime. """
        payload = {}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.put(("http://%s/api/%s/lights/%s/state" % (self.bridge_ip, self.username, light_id)), json.dumps(payload))
        return json.loads(r.text)   
    
    ## Groups
    def _getAllGroups(self):
        r = requests.get(("http://%s/api/%s/groups" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def _createGroup(self, ):
        logging.info("Not yet implemented.")
        
    def _getGroupAttribs(self, group_id):
        r = requests.get(("http://%s/api/%s/groups/%s" % (self.bridge_ip, self.username, group_id)))
        return json.loads(r.text)

    def _setGroupAttribs(self, group_id, **kwargs):
        """ Required: group_id. Optional: name, lights"""
        payload = {}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.put(("http://%s/api/%s/groups/%s" % (self.bridge_ip, self.username, group_id)), json.dumps(payload))
        return json.loads(r.text)

    def _setGroupState(self, group_id, **kwargs):
        """ Required group_id. Optional: on, bri, hue, sat, xy, ct, alert, effect, transiontime. """
        payload = {}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.put(("http://%s/api/%s/groups/%s/action" % (self.bridge_ip, self.username, group_id)), json.dumps(payload))
        return json.loads(r.text)

    def _deleteGroup(self):
        logging.info("Not yet implemented.")

    ## Schedules
    def _getAllSchedules(self):
        r = requests.get(("http://%s/api/%s/schedules" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def _createSchedule(self, command, time, **kwargs):
        """ Required: command, time. Optional: name, description. """
        payload = {'command': command, 'time': time}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.post(("http://%s/api/%s/schedules" % (self.bridge_ip, self.username)), json.dumps(payload))
        return json.loads(r.text)

    def _getScheduleAttribs(self, schedule_id):
        r = requests.get(("http://%s/api/%s/schedules/%s" % (self.bridge_ip, self.username, schedule_id)))
        return json.loads(r.text)

    def _setScheduleAttribs(self, schedule_id, **kwargs):
        """ Required: schedule_id. Optional: name, description, command, time. """
        payload = {}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.put(("http://%s/api/%s/schedules/%s" % (self.bridge_ip, self.username, schedule_id)), json.dumps(payload))
        return json.loads(r.text)

    def _deleteSchedule(self, schedule_id):
        r = requests.delete(("http://%s/api/%s/schedules/%s" % (self.bridge_ip, self.username, schedule_id)))
        return json.loads(r.text)

    ## Config
    def _createUser(self, devicetype, username=None):
        payload = {'devicetype': devicetype}
        if username:
            payload['username'] = username
        
        r = requests.post(("http://%s/api" % (self.bridge_ip)), json.dumps(payload))
        return json.loads(r.text)

    def _getConfig(self):
        r = requests.get(("http://%s/api/%s/config" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def _modifyConfig(self, **kwargs):
        """ Optional: proxyport, name, swupdate, proxyaddress, linkbutton, ipaddress, netmask, gateway, dhcp, portalservices. """
        payload = {}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.put(("http://%s/api/%s/config" % (self.bridge_ip, self.username, schedule_id)), json.dumps(payload))
        return json.loads(r.text)

    def _deleteUserFromWhitelist(self, username):
        r = requests.delete(("http://%s/api/%s/config/whitelist/%s" % (self.bridge_ip, self.username, username)))
        return json.loads(r.text)

    def _getFullState(self):
        r = requests.get(("http://%s/api/%s" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    # Portal API
    def _discoverLocalBridges(self):
        r = requests.get("http://www.meethue.com/api/nupnp")
        return json.loads(r.text)

class Light(object):
    def __init__(self, hue, light_id):
        self.hue = hue
        self.light_id = light_id

        # Colors
        self.red    = 0 
        self.blue   = 46920
        self.green  = 25500
        self.yellow = 12750
        self.purple = 56100
        self.crelax  = 13068
    
    def on(self):
        self.hue._setLightState(self.light_id, on=True)

    def off(self):
        self.hue._setLightState(self.light_id, on=False)
    
    def relax(self):
        self.hue._setLightState(self.light_id, on=True, hue=self.crelax, sat=200, bri=170)

    def alert(self, alert_type="select"):
        self.hue._setLightState(self.light_id, alert=alert_type)
    
    def blinkPurple(self):
        self.blink(self.purple)
    
    def blinkYellow(self):
        self.blink(self.yellow)
    
    def blinkGreen(self):
        self.blink(self.green)
    
    def blinkBlue(self):
        self.blink(self.blue)
    
    def blinkRed(self):
        self.blink(self.red)

    def blink(self, color):
        state = self.hue._getLightAttribsAndState(self.light_id)['state']
        response = self.hue._setLightState(self.light_id, on=True, \
            hue=color, bri=255, sat=255, transiontime=10)
        time.sleep(1)
        response = self.hue._setLightState(self.light_id, on=True, alert="select")
        time.sleep(1)
        self.hue._setLightStateWithPayload(self.light_id, state)
