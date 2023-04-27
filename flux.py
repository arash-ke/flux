#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
import os
import argparse
import yaml
import json
import CloudFlare
import random
from Flux.Config import Config
from Flux.Target import Target
from Flux.Account import Account
from Flux.Record import Record

def pars_args():
  parser = argparse.ArgumentParser(description="A script for implementing flux on cloudflare")
  parser.add_argument("--config", "-c", type=argparse.FileType('r'), default="config.yml")
  args=parser.parse_args()
  return args

def update(target: Target, account: Account):
  cf = account.cf
  zone_id = account.get_zone_id(target.zone)
  for record in target.record_list:
    print("Updating {}".format(record.name))
    params = {
      "name": "{}.{}".format(record.name, target.zone)
    }
    records = cf.zones.dns_records.get(zone_id, params=params)
    current_record = None
    if len(records) > 0:
      for r in records:
        if r['type'] == record.record_type:
          current_record = r
          break
    if current_record != None:
      # update current record
      new_ip = None
      ip_list = random.shuffle(target.ip_list)
      for ip in target.ip_list:
        if ip != current_record['content']:
          new_ip = ip
          break
      if new_ip != None:
        print("Updating current content '{}' with '{}".format(current_record['content'], new_ip))
        params = {
          'content': new_ip,
          'name': record.name,
          'proxied': record.proxied,
          'type': record.record_type,
          'comment': record.comment,
          'tags': record.tags,
          'ttl': record.ttl * 60
        }
        cf.zones.dns_records.put(zone_id, current_record['id'], data=params)
      else:
        print("No new IP selected, current ip: {}.", current_record['content'])
    elif record.create:
      print("Record {} not found. creating one.".format(params['name']))
      params = {
        'content': target.ip_list[0],
        'name': record.name,
        'proxied': record.proxied,
        'type': record.record_type,
        'comment': record.comment,
        'tags': record.tags,
        'ttl': record.ttl * 60
      }
      resp = cf.zones.dns_records.post(zone_id, data=params)
      print("Response: {}".format(resp))
    else:
      print("Record {} not found.".format(params['name']))
def main():
  args = pars_args()
  c = Config(args.config)
  for t in c.targets:
    update(t, c.get_account(t.account))

if __name__ == '__main__':
  main()