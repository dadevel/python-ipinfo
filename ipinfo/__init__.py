from pathlib import Path
from collections import namedtuple
import json
import logging
import os
import socket
import sys
import urllib.request

import maxminddb

IPINFO_TOKEN = os.environ['IPINFO_TOKEN']
IPINFO_EDITION = os.environ.get('IPINFO_EDITION', 'free/country_asn.mmdb')
IPINFO_CACHE = Path(os.environ.get('IPINFO_CACHE', os.environ.get('XDG_CACHE_HOME', Path.home()/'.cache')))/'ipinfo.mmdb'
LOGGER = logging.getLogger('ipinfo')

IpInfo = namedtuple('IpInfo', 'ip_address domain as_domain as_name asn continent continent_name country country_name'.split())


def lookup(query: str, dns: bool = True) -> IpInfo|None:
    if not IPINFO_CACHE.exists():
        LOGGER.info(f'downloading {IPINFO_EDITION} database to {IPINFO_CACHE}')
        urllib.request.urlretrieve(f'https://ipinfo.io/data/{IPINFO_EDITION}?token={IPINFO_TOKEN}', IPINFO_CACHE)
    with maxminddb.open_database(IPINFO_CACHE) as db:
        try:
            data = db.get(query)
            return IpInfo(ip_address=query, domain='', **data) if data else None
        except ValueError as e:
            if not dns:
                raise

        try:
            ip_address = socket.gethostbyname(query)
            data = db.get(ip_address)
            return IpInfo(ip_address=ip_address, domain=query, **data, ) if data else None
        except socket.gaierror:
            return None
        except Exception as e:
            raise e


def main() -> None:
    for line in sys.stdin:
        line = line.rstrip()
        result = lookup(line)
        if result:
            print(json.dumps(result._asdict(), separators=(',', ':')))


if __name__ == '__main__':
    main()
