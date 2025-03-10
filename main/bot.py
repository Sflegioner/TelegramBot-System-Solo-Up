import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from main.handlers.buildbot import start_build
from main.mongo_connection.mogo_connetion import MongoDBConnection

def main():
    start_build()
    db = MongoDBConnection()    

if __name__ == "__main__":
    main() 