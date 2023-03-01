from pathlib import Path
from collections import namedtuple
import urllib.request
import logging
import os

import maxminddb

IPINFO_TOKEN = os.environ['IPINFO_TOKEN']
IPINFO_EDITION = os.environ.get('IPINFO_EDITION', 'free/country_asn.mmdb')
IPINFO_CACHE = Path(os.environ.get('IPINFO_CACHE', os.environ.get('XDG_CACHE_HOME', Path.home()/'.cache')))/'ipinfo.mmdb'
LOGGER = logging.getLogger('ipinfo')

IpInfo = namedtuple('IpInfo', 'as_domain as_name asn continent continent_name country country_name'.split())


def lookup(address: str) -> IpInfo|None:
    if not IPINFO_CACHE.exists():
        LOGGER.info(f'downloading {IPINFO_EDITION} database to {IPINFO_CACHE}')
        urllib.request.urlretrieve(f'https://ipinfo.io/data/{IPINFO_EDITION}?token={IPINFO_TOKEN}', IPINFO_CACHE)
    with maxminddb.open_database(IPINFO_CACHE) as db:
        data = db.get(address)
    return IpInfo(**data) if data else None
