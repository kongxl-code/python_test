from datetime import datetime as dt
from sqlalchemy import Table, MetaData, Column, String, Integer, BigInteger

def defint_pipeline_info_table(table_name):
    metadata = MetaData()
    return Table(table_name, metadata, 
                 Column('id', Integer(), primary_key=True),
                 Column('run_number', Integer(), unique=True, nullable=False),             
                 Column('pipeline_run_id', String(50), unique=True, nullable=False),             
                 Column('start_time', BigInteger()),             
                 Column('end_time', BigInteger())           
                 )