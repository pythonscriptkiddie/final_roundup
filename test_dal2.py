#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 20:39:38 2019

@author: thomassullivan
"""

from datetime import datetime, date
from sqlalchemy import (MetaData, Table, Column, Integer, Numeric, String,
                        DateTime, Date, ForeignKey, Boolean, create_engine,
                        CheckConstraint, insert, select, update)

class DataAccessLayer:
    connection=None
    engine=None
    conn_string = None
    metadata = MetaData()
    articles_table = Table('Articles', metadata,
                    Column('articleID', Integer(), primary_key=True, index=True),
                    Column('name', String(200), default=None),
                    Column('author', String(100), default=None),
                    Column('publication', String(100), default=None),
                    Column('link', String(200), default=None),
                    Column('description', String(500), default=None),
                    Column('date', Date(), default=None),
                    Column('categoryID', ForeignKey('Categories.categoryID'))
                    )

    categories_table = Table('Categories', metadata,
                   Column('categoryID', Integer(), primary_key=True),
                   Column('name', String(50), default=None)
                   )
    def db_init(self, conn_string):
        self.engine = create_engine(conn_string or self.conn_string)
        self.metadata.create_all(self.engine)
        self.connection = self.engine.connect()
    
dal = DataAccessLayer()
#All communication to and from the database will take place through the
#DataAccessLayer
    
#engine = create_engine('sqlite:///db2.db')
#metadata.create_all(engine)
#connection = engine.connect()
