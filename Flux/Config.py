#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

# import sys
import os
import yaml
# import CloudFlare
# import netifaces
from .Target import Target
from .Account import Account

class Config:
  __config_data = None
  __targets = []
  __accounts = {}
  
  def __init__(self, conf_file):
    file_name, file_extension = os.path.splitext(conf_file.name)
    file_name = file_name.lower()
    file_extension = file_extension.lower()
    if file_extension == '.yaml' or file_extension == '.yml':
      self.__config_data = yaml.safe_load(conf_file)
    for n, a in self.config_data['accounts'].items():
      account = Account(a)
      self.__accounts[n] = account
      print("Added account: {}".format(n))
    for t in self.config_data['targets']:
      target = Target(t)
      self.__targets.append(target)

  @property
  def config_data(self):
    return(self.__config_data)

  @property
  def targets(self):
    return self.__targets
  
  def get_account(self, name):
    return self.__accounts[name]