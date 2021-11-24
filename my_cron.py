import configparser
import logging
import logging.config
import my_cron_config_reader
import os
import signal
import time
from crontab import CronTab
from croniter import croniter
from datetime import datetime

SLEEP_INTERVAL = int(59)

dir_name, f_name = os.path.split(__file__)


def logger_setup():
    if(os.path.isfile(dir_name+"/logging.conf")):
        try:
            logging.config.fileConfig(dir_name+'/logging.conf')
        except Exception:
            print("Config file "+dir_name+'/logging.conf'+" Not Found")
            logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s",
                                filename=dir_name+'/cron_parser.log', level=logging.DEBUG)

    else:
        logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s",
                            filename=dir_name+'/cron_parser.log', level=logging.DEBUG)

def cron_starter():
    while True:
        logger.info("Try to read cron file")

        try:
            cron = CronTab(
                tabfile=this_config["cron_settings"]['cron_path']+this_config["cron_settings"]['username'], user=False)
        except Exception as e:
            logger.error(e)
            exit(-1)

        logger.info("Trying run commands")

        try:
            for job in cron:
                logger.debug("Will check this time: "+str(job.slices))
                if croniter.match(str(job.slices), datetime.now()):
                    logger.debug(
                        "Entered into task with time "+str(job.slices))
                    logger.debug("Will run command: "+str(job.command))
                    try:
                        pid = os.fork()
                    except OSError as e:
                        logger.error(e)
                    if (pid == 0):
                        try:
                            os.system(job.command)
                            logger.info("Command "+str(job.command) +
                                        " completed successfully")
                        except OSError as e:
                            logger.error(e)
                        finally:
                            os.kill(os.getpid(), signal.SIGKILL)
                logger.info("Go to the next time")
        except Exception as e:
            logger.error(e)
        time.sleep(SLEEP_INTERVAL)


logger_setup()
logger = logging.getLogger(__name__)

parseconfig = configparser.ConfigParser()
logger.info("Configured configparser")

try:
    this_config = my_cron_config_reader.read_json_conf(logger)
    logger.debug("Config file: "+str(this_config))
    cron_starter()

except Exception as e:
    logger.error(e)
