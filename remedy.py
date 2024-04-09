#!/usr/bin/env python
######## -*- coding: utf-8 -*
import xml.etree.ElementTree as ET
import os, sys, time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


apps = [('remedy','https://prodremedy.prod.oami.eu:8443/arsys/forms/itsmohim/SHR%3ALandingConsole/Default+Administrator+View/?cacheid=b2af5e14'),
        ('smartit','https://myservicedesk.prod.oami.eu:8443/ux/smart-it/#/'),
        ('myit','https://myservicedesk.prod.oami.eu:8443/ux/myitapp/#/')]
xmlPath = '/home/opsmon/scripts/remedy/health/'

for app in apps:
	xmlFile = app[0] + '_alert.xml'
	root = ET.Element(app[0])
	comment = ET.Comment('This XML is generated by a script called remedy.py at ocvlp-bmc014. In case of malfunction or further changes check the script there.')
	root.insert(1, comment)
	root.set('time', str(time.time()))

	alert = ET.SubElement(root, 'alert')
	alert.set('link', app[1])
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        page = requests.get(app[1], verify=False, allow_redirects=False)
	ET.SubElement(alert, 'status_code').text = str(page.status_code)
        if page.status_code == 401 or page.status_code == 200 or page.status_code  == 302:
        	ET.SubElement(alert, 'status').text = 'OK'
	else:
        	ET.SubElement(alert, 'status').text = 'NotOK'

        dataAlarm =  ET.tostring(root).decode("utf-8")
	fileAlarm = open(xmlPath +  xmlFile, 'w')
	fileAlarm.write(dataAlarm)
	fileAlarm.close()

