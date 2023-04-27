#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# import sys
# import os
# import argparse
# import yaml
import CloudFlare as CF
# import netifaces

class Account:
  __api_token: None
  __cf = None
  __zones = {}
  
  def __init__(self, account):
    for k, v in account.items():
      setattr(self, k, v)
    try:
      self.cf = CF.CloudFlare(token=self.api_token)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
      exit('/zones %d %s - api call failed' % (e, e))
    except Exception as e:
      exit('/zones.get - %s - api call failed' % (e))
    zones = self.cf.zones.get()
    for z in zones:
      self.zones[z['name']] = z
  
  @property
  def api_token(self):
    return self.__api_token
  @api_token.setter
  def api_token(self, v):
    self.__api_token = v

  def __get_cf(self):
    return self.__cf
  def __set_cf(self, v):
    self.__cf = v
  cf = property(__get_cf, __set_cf)

  def get_zones(self):
    return self.__zones
  def __set_zones(self, v):
    self.__zones = v
  zones = property(get_zones, __set_zones)
  
  def get_zone_id(self, zone):
    return self.zones[zone]['id']