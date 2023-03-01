# python-ipinfo

Create a free account at [ipinfo.io](https://ipinfo.io/) and note your access token.
Then proceed with the example below.

~~~
❯ export IPINFO_TOKEN=0123456789abcd
❯ pip3 install --user git+https://github.com/dadevel/python-ipinfo.git@main
❯ python3
>>> import ipinfo
>>> info = ipinfo.lookup('1.1.1.1')
>>> print(info)
IpInfo(as_domain='cloudflare.com', as_name='Cloudflare, Inc.', asn='AS13335', continent='NA', continent_name='North America', country='US', country_name='United States')
~~~
