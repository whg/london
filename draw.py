# hint: this is python 3

from pyx import *
import math

c = canvas.canvas()

import os
import sqlite3 as lite
from lxml import html

conn = lite.connect('london.db')
cursor = conn.cursor()

places = cursor.execute('select id, name, x, y from london_places;').fetchall()

for id, name, x, y in places:
    d = 50
    print(name)
    col = color.rgb(0, 0, 0)
    if name == 'Finsbury':
        col = color.rgb(1, 0.3, 0)
    if name == 'Islington':
        col = color.rgb(0.1, 0.8, 0)
    c.fill(path.circle(x*d, y*d, 0.1), [col])

c.writePDFfile('out.pdf')
