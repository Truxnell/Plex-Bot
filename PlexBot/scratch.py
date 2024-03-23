import logging
import sys
from pathlib import Path
from typing import Dict
from plexapi.exceptions import Unauthorized
from plexapi.exceptions import NotFound
from plexapi.server import PlexServer

import yaml

FORMAT = "%(asctime)s %(levelname)s: [%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"

logging.basicConfig(format=FORMAT)
log = logging.getLogger("Bot")
log.setLevel("DEBUG")

def load_config(basedir: str,filename: str) -> Dict[str, str]:
    filename = Path(basedir, filename)
    try:
        with open(filename, "r") as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError:
        log.fatal("Configuration file not found at '"+str(filename)+"'.")
        sys.exit(-1)

    return config

if __name__ == "__main__":
  
    configdir = "config"
    log.info(f'Loading {configdir} config.yaml')
    config = load_config(configdir,"config.yaml")

    base_url = config["plex"]["base_url"]
    plex_token = config["plex"]["token"]
    library_name = config["plex"]["library_name"]

    # Log fatal invalid plex token
    log.debug(f"Connecting to Plex at '{base_url}'")
    try:
        plex = PlexServer(base_url, plex_token)
    except Unauthorized:
        log.fatal("Invalid Plex token, stopping...")
        raise Unauthorized("Invalid Plex token")

    music = plex.library("Music")
    
