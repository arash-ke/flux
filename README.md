# Ansible Base
Simple script to change DNS record at Cloudflare.
You can have multiple account and assign a target to an account. each target can update single zone and multiple records.

This script will go through all targets defined on ```targets``` field off config file. For each target it will generate a list of IP using ```ip``` definition of target, then look for existing record of zone in defined CloudFlare account.
If record is present in zone then it will be updated, if not and ```create``` is set to true for record, it will create new record.
this script will update firs record that matches ```name``` and ```record_type``` on record.
IP assignment policy is, it will randomly select an IP from generated list of IP and if the selected IP is different than current IP of record it will be updated, otherwise it will select another next random IP. If there isn't any new IP in list, no update will happen.

## Usage

Install requirements.txt.
```bash
pip install -r requirements.txt
```

Simply run using following command after you created your config file.
```bash
python flux.py
```

Available argumants are as follow:
```bash
# python flux.py -h
usage: flux.py [-h] [--config CONFIG]

A script for implementing flux on cloudflare

optional arguments:
  -h, --help            show this help message and exit
  --config CONFIG, -c CONFIG
  --config CONFIG, -c CONFIG
```

### Config file

Default config file is config.yml.

```yaml
---
accounts: # CloudFlare accounts.
  main: # Account name. this field is used on targets.
    api_token: mQmWs6HWKYRx0IpABwSPxTCtzkTd46wmGiDCiJOe # API token from CloudFlare.
targets: # Targets.
  - account: main # CloudFlare account to use.
    zone: example.com # Zone to work on.
    records: # Records to proccess.
      - record_type: A # Record type, Mandatory.
        name: test # Record name. Mandatory.
        create: false # Create the record if it's not already defined, Default: false.
        proxied: false # Set record as proxied in CloudFlare. Default: false.
        comment: "Updated using flux script" # Record comment. Default "".
        ttl: 3 # Record TTL in minutes. Default: 1
    ip: # List of IP's to choose from.
      jsonMyIp: # Use a JSON Api. Optional.
        - url: https://api.myip.com/ # URL of json API endpoint.
          field: ip # Field in json response.
      interfaces: # Interfaces to get IP from. Optional.
        - eth0
      list: # List of IP's. Optional
        - 192.168.0.1
```
