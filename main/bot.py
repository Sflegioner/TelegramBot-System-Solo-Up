import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main.handlers.buildbot import start_build
from main.mongo_connection.mogo_connetion import MongoDBConnection
from main.logger.logger_base_conf import setup_logger

def main():
    logger = setup_logger()
    logger.info("Starting bot...")
    db = MongoDBConnection()    
    start_build()

if __name__ == "__main__":
    main() 