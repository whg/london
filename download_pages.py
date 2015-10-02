import json
import urllib2
import math
import sqlite3 as lite
from lxml import html

data = json.loads(open('boroughs.json').read())

def name_from_link(link):
    return link.split('/')[-1]

def lat2y(a):
  return 180.0/math.pi*math.log(math.tan(math.pi/4.0+a*(math.pi/180.0)/2.0))

def get_pages():
    links = set([e['link'] for e in data])

    for link in links:
        try:
            response = urllib2.urlopen('https://en.wikipedia.org' + link)
            print 'downloaded %s' % (link),

            with open('pages/%s' % name_from_link(link), 'w') as f:
                f.write(response.read())

            print 'wrote'

        except:
            print 'failed on %s' % link


def insert_into_db():
    con = lite.connect('london.db')

    def db_row(place):
        name = urllib2.unquote(place['name'])

        try:
            e = html.parse('pages/%s' % name_from_link(place['link']))
            latlon = e.xpath('//*[@id="coordinates"]/span/a/span[3]/span[2]/span')[0].text.split(';')
        except IndexError:
            return False
            
        lat = float(latlon[0])
        lon = float(latlon[1])

        print 'found %s' % (name)

        return (name, place['borough'], place['link'], lat, lon, lon, lat2y(lat))


    rows = filter(None, map(db_row, data))
    
    
    qs = ','.join(['?']*len(rows[0]))
    
    with con:
        cur = con.cursor()
        cur.executemany("INSERT INTO places (name, borough, link, lat, lon, x, y) VALUES(%s)" % qs, rows)

        print 'inserted %d rows into places (%d links)' % (len(rows), len(data))


def second_order():
    con = lite.connect('london.db')

    def wiki_links((id, name, link)):
        try:
            e = html.parse('pages/%s' % name_from_link(link))
            valid_links = [l for l in e.xpath('//*[@id="mw-content-text"]//a/@href')
                           if l.startswith('/wiki')]
            return (name, id, valid_links)
        except IndexError:
            return False
        
    
            
    with con:
        cur = con.cursor()
        rows = cur.execute('SELECT id, name, link FROM places').fetchall()

        q = filter(None, map(wiki_links, rows))
        for name, id, links in q:
            for link in links:
                cur.execute('INSERT INTO links (from_name, from_id, to_link) VALUES(?,?,?)', (name, id, link))
            print 'added %d links for %s' % (len(links), name)
    


            
if __name__ == "__main__":
    
    # insert_into_db()
    # second_order()
