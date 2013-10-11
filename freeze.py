#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_frozen import Freezer
from app import app
import os
import pymongo
from pymongo.errors import ConnectionFailure
MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:  # on Heroku, get a connection
	m_conn = pymongo.Connection(MONGO_URL)
	db = m_conn[urlparse(MONGO_URL).path[1:]]
	RUNNING_LOCAL = False
else:  # work locally
	try:
		m_conn = pymongo.Connection('localhost', 27017)
	except ConnectionFailure:
		print('You should have mongodb running')

	db = m_conn['citymap']
	RUNNING_LOCAL = True
	app.debug = True  # since we're local, keep debug on

freezer = Freezer(app)
@freezer.register_generator
def gushim_details():
    for gush in db.gushim.find():
        gush_id = gush['gush_id']
        yield {'gush_id':gush_id}

if __name__ == '__main__':
    freezer.freeze()
