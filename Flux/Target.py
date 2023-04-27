#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import requests
import netifaces
import json
from .Record import Record

class Target:
  __data = None
  __ip_list = []
  __record_list = []
  __zone = None
  __account = None

  def __init__(self, t):
    self.__data = t
    
    self.__zone = self.__data['zone']
    self.__account = self.__data['account']
    
    if 'list' in self.__data['ip']:
      self.__ip_list.extend(self.__data['ip']['list'])
    if 'interfaces' in self.__data['ip']:
      ifaces = netifaces.interfaces()
      for i in self.__data['ip']['interfaces']:
        if i in ifaces:
          addresses = netifaces.ifaddresses(i)[netifaces.AF_INET]
          for a in addresses:
            self.__ip_list.append(a['addr'])
    if 'jsonMyIp' in self.__data['ip']:
      for j in self.__data['ip']['jsonMyIp']:
        r = requests.get(j['url'])
        if r.ok and r.status_code == 200:
          ip = json.loads(r.text)[j['field']]
          self.__ip_list.append(ip)
    for r in self.__data['records']:
      record = Record(r)
      self.__record_list.append(record)

  @property
  def ip_list(self):
    return self.__ip_list

  @property
  def record_list(self):
    return self.__record_list

  @property
  def account(self):
    return self.__account
  
  @property
  def zone(self):
    return self.__zone