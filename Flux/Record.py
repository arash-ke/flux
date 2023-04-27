#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

class Record:
  __record_type = None
  __name = None
  __ttl = 1
  __create = False
  __proxied = False
  __comment = ""
  __tags = []
  
  def __init__(self, record):
    for k, v in record.items():
      setattr(self, k, v)
  
  def __str__(self):
    return "{} IN {} {}".format(self.name, self.record_type, self.ttl)
  
  @property
  def record_type(self):
    return self.__record_type
  @record_type.setter
  def record_type(self, v):
    self.__record_type = v
  
  @property
  def name(self):
    return self.__name
  @name.setter
  def name(self, v):
    self.__name = v
  
  @property
  def ttl(self):
    return self.__ttl
  @ttl.setter
  def ttl(self, v):
    self.__ttl = v

  @property
  def create(self):
    return self.__create
  @create.setter
  def create(self, v):
    self.__create = v
  
  @property
  def proxied(self):
    return self.__proxied
  @proxied.setter
  def proxied(self, v):
    self.__proxied = v
    
  @property
  def comment(self):
    return self.__comment
  @comment.setter
  def comment(self, v):
    self.__comment = v
    
  @property
  def tags(self):
    return self.__tags
  @tags.setter
  def tags(self, v):
    self.__tags = v