# -*- coding: utf-8 -*-
"""
    Application to change cloudflare DNS record using different IP sources
"""
from __future__ import absolute_import, division, print_function


import argparse
import random
from Flux.Config import Config
from Flux.Target import Target
from Flux.Account import Account


def pars_args():
    """_summary_

    Returns:
        _type_: _description_
    """
    parser = argparse.ArgumentParser(
        description="A script for implementing flux on cloudflare"
    )
    parser.add_argument(
        "--config", "-c", type=argparse.FileType("r"), default="config.yml"
    )
    args = parser.parse_args()
    return args

def update(target: Target, account: Account):
    """_summary_

    Args:
        target (Target): _description_
        account (Account): _description_
    """
    cf = account.cf
    zone_id = account.get_zone_id(target.zone)
    for record in target.record_list:
        print(f"Updating {record.name}")
        params = {"name": f"{record.name}.{target.zone}"}
        records = cf.zones.dns_records.get(zone_id, params=params)
        current_record = None
        for r in records:
            if r["type"] == record.record_type:
                current_record = r
                break
        if current_record is not None:
            # update current record
            new_ip = None
            target.ip_list.remove(current_record['content'])
            if len(target.ip_list) > 1:
                random.shuffle(target.ip_list)
                new_ip = target.ip_list[0]
                print(f"Updating current content '{current_record['content']}' with '{new_ip}'")
                params = {
                    "content": new_ip,
                    "name": record.name,
                    "proxied": record.proxied,
                    "type": record.record_type,
                    "comment": record.comment,
                    "tags": record.tags,
                    "ttl": record.ttl * 60,
                }
                cf.zones.dns_records.put(zone_id, current_record["id"], data=params)
            else:
                print(f"No new IP selected, current ip: {current_record['content']}.")
        elif record.create:
            print(f"Record {params['name']} not found. creating one.")
            params = {
                "content": target.ip_list[0],
                "name": record.name,
                "proxied": record.proxied,
                "type": record.record_type,
                "comment": record.comment,
                "tags": record.tags,
                "ttl": record.ttl * 60,
            }
            resp = cf.zones.dns_records.post(zone_id, data=params)
            print(f"Response: {resp}")
        else:
            print(f"Record {params['name']} not found.")


def main():
    """_summary_
    """
    args = pars_args()
    c = Config(args.config)
    for t in c.targets:
        update(t, c.get_account(t.account))


if __name__ == "__main__":
    main()
