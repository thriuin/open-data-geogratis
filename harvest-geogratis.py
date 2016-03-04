from ConfigParser import ConfigParser
from contextlib import contextmanager
from database import GrtsRecordTable, GrtsSettingTable, get_setting, get_session, save_setting
from lxml import etree
from lxml.etree import Element

import requests


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = get_session()()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def get_config(section, key):
    conf = ConfigParser()
    conf.read('open-data-geogratis.ini')
    return conf.get(section, key)


def read_geogratis_feed(grts_url):

    _links = {}
    _geo_ns = {'atom': 'http://www.w3.org/2005/Atom',
               'os': 'http://a9.com/-/spec/opensearch/1.1/',
               'as': 'http://atomserver.org/namespaces/1.0/',
               'georss': 'http://www.georss.org/georss',
               'gml': 'http://www.opengis.net/gml'}

    def _read_links(root):
        link_query = etree.ETXPath('{%s}link' % _geo_ns['atom'])
        links = link_query(root)

        for link in links:
            rel = link.get('rel')
            if rel == 'next':
                _links['next_url'] = link.get('href')
            elif rel == 'monitor':
                _links['monitor_url'] = link.get('href')

    r = requests.get(grts_url)
    if r.status_code == 200:

        root = etree.fromstring(r.content)
        #print etree.tostring(root, pretty_print=True)
        _read_links(root)
        # @todo Start here
    else:
        print "Web error: response: '%d', reason: '%s', url: '%s'" % r.status_code, r.reason, r.url


def main():
    base_url = get_config('geogratis', 'baseurl')
    print base_url
    read_geogratis_feed("%s/?max-results=100&alt=xml" % base_url)

#    with session_scope() as session:
#        save_setting('last_geogratis_baseurl', base_url, session)

    #get_setting("geogratis_link", session)

main()

