import json
import logging
import os

dir_name, f_name = os.path.split(__file__)


def read_json_conf(logger):
    logger.info("Try for read json config file")
    logger.debug("Path to the json config file: " +
                 dir_name+"/cron_parser_config.json")

    this_config = {}

    try:
        if(os.path.isfile(dir_name+"/cron_parser_config.json")):
            file = open(dir_name+"/cron_parser_config.json")
            this_config = json.loads(file.read())
        else:
            this_config = {"cron_settings": {"cron_path": "/var/spool/cron/crontabs/", "username": "a"},
                           "logging_settings": {"file_name": "/configparser.log", "logging_level": 10}}
    except IOError as e:
        logger.error(e)
        logger.info("Will configure default config")
        this_config = {"cron_settings": {"cron_path": "/var/spool/cron/crontabs/", "username": "a"},
                       "logging_settings": {"file_name": "/configparser.log", "logging_level": 10}}

    logger.debug("Config file: "+str(this_config))
    return this_config
