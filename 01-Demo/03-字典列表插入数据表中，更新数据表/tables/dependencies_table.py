from datetime import datetime as dt
from sqlalchemy import Table, MetaData, Column, String, Integer, BigInteger, Boolean

def defint_dependencies_table(table_name):
    metadata = MetaData()
    return Table(table_name, metadata, 
                 Column('id', Integer(), primary_key=True),
                 Column('module', String(20), nullable=False),             
                 Column('dependency', String(20), nullable=False),             
                 Column('status', Boolean()),             
                 Column('update_on', BigInteger(), default=dt.now().timestamp(), onupdate=dt.now().timestamp()),             
                 )