"""Setup the network-pinger application"""
import logging

from networkpinger.model import meta
log = logging.getLogger(__name__)

def setup_app():
    """Place any commands to setup networkpinger here"""
    log.info("Creating tables..")
    # Create the tables if they don't already exist
    meta.metadata.create_all(bind=meta.engine)
