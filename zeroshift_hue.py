#!/usr/bin/env python

import json
import requests
import sys, time

class Hue(object):
    def __init__(self, devicetype="zeroshift-hue", username=None, bridge_ip=None):
        self.bridge_ip = bridge_ip
        if not self.bridge_ip:
          self.bridge_ip = self.getBridgeIP() 
        
        self.devicetype = devicetype
        self.username = username

        # Colors
        self.red    = 0 
        self.blue   = 46920
        self.green  = 25500
        self.yellow = 12750
        self.purple = 56100
        self.crelax  = 13068

    def getBridgeIP(self): 
        try:
            response = self.discoverLocalBridges()
            bridge_ip = response[0]['internalipaddress']
            print "Discovered bridge. IP: %s" % bridge_ip
            return bridge_ip
        except:
            print "Could not get bridge IP!"
            return False

    def authenticate(self):
        if self.username:
            return self.username
        else:
            response = self.createUser(self.devicetype)
            # Note: Fix this. It's ugly
            try:
                if response[0]['error']:
                    print "Warning: %" % response[0]['error']['description']
                    return False
            except:
                pass
            try:
                if response[0]['success']:
                    self.username = response[0]['success']['username']
                    return self.username
            except:
                return False

    # Custom
    def off(self):
        for light in self.getAllLights():
            self.setLightState(light, on=False)
    
    def relax(self):
        for light in self.getAllLights():
            self.setLightState(light, on=True, hue=self.crelax, sat=200, bri=170)

    def alert(self, light_id, alert_long=False):
        alert_type = "select"
        if alert_long:
            alert_type = "lselect"

        if light_id == "all":
            for light in self.getAllLights():
                self.setLightState(light, alert=alert_type)
        else:
            self.setLightState(light_id, alert=alert_type)
    
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
        states = {}
        lights = self.getAllLights()
        for light in lights:
            states[light] = self.getLightAttribsAndState(light)['state']
            
        for light in lights:
            response = self.setLightState(light, on=True, hue=color, bri=255, sat=255, transiontime=10)
        
        time.sleep(1)

        for light in lights:
            response = self.setLightState(light, on=True, alert="select")

        time.sleep(1)

        for light in lights:
            self.setLightStateWithPayload(light, states[light])

    def getLightState(self, light_id):
        r = requests.get(("http://%s/api/%s/lights/%s" % (self.bridge_ip, self.username, light_id)))
        return json.loads(r.text)['state']

    def setLightStateWithPayload(self, light_id, payload):
        r = requests.put(("http://%s/api/%s/lights/%s/state" % (self.bridge_ip, self.username, light_id)), json.dumps(payload))
        return json.loads(r.text)

    # Lights
    def getAllLights(self):
        r = requests.get(("http://%s/api/%s/lights" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def getNewLights(self):
        r = requests.get(("http://%s/api/%s/lights/new" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def searchNewLights(self):
        r = requests.post(("http://%s/api/%s/lights" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def getLightAttribsAndState(self, light_id):
        r = requests.get(("http://%s/api/%s/lights/%s" % (self.bridge_ip, self.username, light_id)))
        return json.loads(r.text)

    def setLightName(self, light_id, name):
        payload = {'name': name}
        r = requests.put(("http://%s/api/%s/lights/%s" % (self.bridge_ip, self.username, light_id)), json.dumps(payload))
        return json.loads(r.text)

    def setLightState(self, light_id, **kwargs):
        """ Required: light_id. Optional: on, bri, hue, sat, xy, ct, alert, effect, transiontime. """
        payload = {}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.put(("http://%s/api/%s/lights/%s/state" % (self.bridge_ip, self.username, light_id)), json.dumps(payload))
        return json.loads(r.text)   
    
    ## Groups
    def getAllGroups(self):
        r = requests.get(("http://%s/api/%s/groups" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def createGroup(self, ):
        print "Not yet implemented." 
        
    def getGroupAttribs(self, group_id):
        r = requests.get(("http://%s/api/%s/groups/%s" % (self.bridge_ip, self.username, group_id)))
        return json.loads(r.text)

    def setGroupAttribs(self, group_id, **kwargs):
        """ Required: group_id. Optional: name, lights"""
        payload = {}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.put(("http://%s/api/%s/groups/%s" % (self.bridge_ip, self.username, group_id)), json.dumps(payload))
        return json.loads(r.text)

    def setGroupState(self, group_id, **kwargs):
        """ Required group_id. Optional: on, bri, hue, sat, xy, ct, alert, effect, transiontime. """
        payload = {}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.put(("http://%s/api/%s/groups/%s/action" % (self.bridge_ip, self.username, group_id)), json.dumps(payload))
        return json.loads(r.text)

    def deleteGroup(self):
        print "Not yet implemented." 

    ## Schedules
    def getAllSchedules(self):
        r = requests.get(("http://%s/api/%s/schedules" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def createSchedule(self, command, time, **kwargs):
        """ Required: command, time. Optional: name, description. """
        payload = {'command': command, 'time': time}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.post(("http://%s/api/%s/schedules" % (self.bridge_ip, self.username)), json.dumps(payload))
        return json.loads(r.text)

    def getScheduleAttribs(self, schedule_id):
        r = requests.get(("http://%s/api/%s/schedules/%s" % (self.bridge_ip, self.username, schedule_id)))
        return json.loads(r.text)

    def setScheduleAttribs(self, schedule_id, **kwargs):
        """ Required: schedule_id. Optional: name, description, command, time. """
        payload = {}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.put(("http://%s/api/%s/schedules/%s" % (self.bridge_ip, self.username, schedule_id)), json.dumps(payload))
        return json.loads(r.text)

    def deleteSchedule(self, schedule_id):
        r = requests.delete(("http://%s/api/%s/schedules/%s" % (self.bridge_ip, self.username, schedule_id)))
        return json.loads(r.text)

    ## Config
    def createUser(self, devicetype, username=None):
        payload = {'devicetype': devicetype}
        if username:
            payload['username'] = username
        
        r = requests.post(("http://%s/api" % (self.bridge_ip)), json.dumps(payload))
        return json.loads(r.text)

    def getConfig(self):
        r = requests.get(("http://%s/api/%s/config" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    def modifyConfig(self, **kwargs):
        """ Optional: proxyport, name, swupdate, proxyaddress, linkbutton, ipaddress, netmask, gateway, dhcp, portalservices. """
        payload = {}
        for key,value in kwargs.items():
            payload[key] = value
        r = requests.put(("http://%s/api/%s/config" % (self.bridge_ip, self.username, schedule_id)), json.dumps(payload))
        return json.loads(r.text)

    def deleteUserFromWhitelist(self, username):
        r = requests.delete(("http://%s/api/%s/config/whitelist/%s" % (self.bridge_ip, self.username, username)))
        return json.loads(r.text)

    def getFullState(self):
        r = requests.get(("http://%s/api/%s" % (self.bridge_ip, self.username)))
        return json.loads(r.text)

    # Portal API
    def discoverLocalBridges(self):
        r = requests.get("http://www.meethue.com/api/nupnp")
        return json.loads(r.text)
