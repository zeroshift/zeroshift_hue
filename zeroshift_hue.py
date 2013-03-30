#!/usr/bin/env python

import json
import requests
import sys

class Hue(object):
    def __init__(self, username=None):
        self.bridge_ip = self.getBridgeIP() 
        #self.username = username
        self.username = "29b66ed65c38720d0ab3a21749c9b"

    def getBridgeIP(self): 
        try:
            response = self.discoverLocalBridges()
            bridge_ip = response[0]['internalipaddress']
            print "Found bridge: %s" % bridge_ip
            return bridge_ip
        except:
            print "Could not get bridge IP!"
            sys.exit(1)    

    def authenticate(self):
        if not self.username:
            response = self.createUser("macbook")
            try:
                if response[0]['error']:
                    print response[0]['error']['description']
                    return False
            except:
                pass
            try:
                if response[0]['success']:
                    self.username = response[0]['success']['username']
                    print "Username: %s" % self.username
                    return True
            except:
                return False
        else:
            return True
    # Custom
    def blinkRed(self):
        states = {}
        lights = self.getAllLights()
        for light in lights:
            states[light] = self.getLightAttribsAndState(light)['state']
            
        for light in lights:
            response = self.setLightState(light, on=True, alert="select", xy=[0.64843, 0.33086])
            print response

        for light in lights:
            self.setLightStatePayload(light, states[light])

    # Lights
    def getAllLights(self):
        try:
            r = requests.get(("http://%s/api/%s/lights" % (self.bridge_ip, self.username)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def getNewLights(self):
        try:
            r = requests.get(("http://%s/api/%s/lights/new" % (self.bridge_ip, self.username)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def searchNewLights(self):
        try:
            r = requests.post(("http://%s/api/%s/lights" % (self.bridge_ip, self.username)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def getLightAttribsAndState(self, light_id):
        try:
            r = requests.get(("http://%s/api/%s/lights/%s" % (self.bridge_ip, self.username, light_id)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def setLightName(self, light_id, name):
        try:
            payload = {'name': name}
            r = requests.put(("http://%s/api/%s/lights/%s" % (self.bridge_ip, self.username, light_id)), json.dumps(payload))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def setLightState(self, light_id, **kwargs):
        """ Required: light_id. Optional: on, bri, hue, sat, xy, ct, alert, effect, transiontime. """
        try:
            payload = {}
            for key,value in kwargs.items():
                payload[key] = value
            r = requests.put(("http://%s/api/%s/lights/%s/state" % (self.bridge_ip, self.username, light_id)), json.dumps(payload))
            return json.loads(r.text)   
        except Exception, e:
            print e
            return False
    
    def setLightStatePayload(self, light_id, payload):
        try:
            r = requests.put(("http://%s/api/%s/lights/%s/state" % (self.bridge_ip, self.username, light_id)), json.dumps(payload))
            return json.loads(r.text)   
        except Exception, e:
            print e
            return False

    ## Groups
    def getAllGroups(self):
        try:
            r = requests.get(("http://%s/api/%s/groups" % (self.bridge_ip, self.username)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def createGroup(self, ):
        print "Not yet implemented." 
        
    def getGroupAttribs(self, group_id):
        try:
            r = requests.get(("http://%s/api/%s/groups/%s" % (self.bridge_ip, self.username, group_id)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def setGroupAttribs(self, group_id, **kwargs):
        """ Required: group_id. Optional: name, lights"""
        try:
            payload = {}
            for key,value in kwargs.items():
                payload[key] = value
            r = requests.put(("http://%s/api/%s/groups/%s" % (self.bridge_ip, self.username, group_id)), json.dumps(payload))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def setGroupState(self, group_id, **kwargs):
        """ Required group_id. Optional: on, bri, hue, sat, xy, ct, alert, effect, transiontime. """
        try:
            payload = {}
            for key,value in kwargs.items():
                payload[key] = value
            r = requests.put(("http://%s/api/%s/groups/%s/action" % (self.bridge_ip, self.username, group_id)), json.dumps(payload))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def deleteGroup(self):
        print "Not yet implemented." 

    ## Schedules
    def getAllSchedules(self):
        try:
            r = requests.get(("http://%s/api/%s/schedules" % (self.bridge_ip, self.username)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def createSchedule(self, command, time, **kwargs):
        """ Required: command, time. Optional: name, description. """
        try:
            payload = {'command': command, 'time': time}
            for key,value in kwargs.items():
                payload[key] = value
            r = requests.post(("http://%s/api/%s/schedules" % (self.bridge_ip, self.username)), json.dumps(payload))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def getScheduleAttribs(self, schedule_id):
        try:
            r = requests.get(("http://%s/api/%s/schedules/%s" % (self.bridge_ip, self.username, schedule_id)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def setScheduleAttribs(self, schedule_id, **kwargs):
        """ Required: schedule_id. Optional: name, description, command, time. """
        try:
            payload = {}
            for key,value in kwargs.items():
                payload[key] = value
            r = requests.put(("http://%s/api/%s/schedules/%s" % (self.bridge_ip, self.username, schedule_id)), json.dumps(payload))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def deleteSchedule(self, schedule_id):
        try:
            r = requests.delete(("http://%s/api/%s/schedules/%s" % (self.bridge_ip, self.username, schedule_id)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    ## Config
    def createUser(self, devicetype, username=None):
        try:
            payload = {'devicetype': devicetype}
            if username:
                payload['username'] = username
            
            r = requests.post(("http://%s/api" % (self.bridge_ip)), json.dumps(payload))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def getConfig(self):
        try:
            r = requests.get(("http://%s/api/%s/config" % (self.bridge_ip, self.username)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def modifyConfig(self, **kwargs):
        """ Optional: proxyport, name, swupdate, proxyaddress, linkbutton, ipaddress, netmask, gateway, dhcp, portalservices. """
        try:
            payload = {}
            for key,value in kwargs.items():
                payload[key] = value
            r = requests.put(("http://%s/api/%s/config" % (self.bridge_ip, self.username, schedule_id)), json.dumps(payload))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def deleteUserFromWhitelist(self, username):
        try:
            r = requests.delete(("http://%s/api/%s/config/whitelist/%s" % (self.bridge_ip, self.username, username)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    def getFullState(self):
        try:
            r = requests.get(("http://%s/api/%s" % (self.bridge_ip, self.username)))
            return json.loads(r.text)
        except Exception, e:
            print e
            return False

    # Portal API
    def discoverLocalBridges(self):
        r = requests.get("http://www.meethue.com/api/nupnp")
        return json.loads(r.text)
