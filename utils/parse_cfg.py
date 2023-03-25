"""Parse the configuration file."""

import json
import os
import logging
import datetime
import pytz

logger = logging.getLogger(__name__)

def parse_timezone(config):
    """Convert the timezone string to datetime.timezone"""
    tz = pytz.timezone(config['timezone'])
    return tz

def parse_cfg(cfg_path='temp/config.json'):
    """Parse the configuration file."""
    with open(cfg_path, 'rt', encoding='UTF-8') as cfg:
        config = json.load(cfg)

    tz = parse_timezone(config=config)

    return {
        'timezone': tz, 
        'spreadsheet_id': config['spreadsheet_id'], 
        'sheet_name': config['sheet_name'],
        'summary_name': config['summary_name'],
        "share_link": config["share_link"],
        }