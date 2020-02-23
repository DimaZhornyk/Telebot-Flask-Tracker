from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, DateTime

engine = create_engine("sqlite:///db.sqlite")
metadata = MetaData()
Global = Table('Global', metadata,
               Column('id', Integer),
               Column('name', String),
               Column('surname', String),
               Column('total_hours', Integer),
               Column('total_minutes', Integer),
               Column('total_seconds', Integer),
               Column('last_project', String),
               Column('last_job', String),
               Column('lastLat', Float),
               Column('lastLng', Float),
               Column("project_chosen", String))
Locations = Table('Locations', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String),
                  Column('lat', Float),
                  Column('lng', Float)
                  )
Users = Table('Users', metadata,
              Column('id', Integer, primary_key=True),
              Column('username', String),
              Column('password', String))
History = Table('History', metadata,
                Column('user_id', Integer),
                Column('hours', Integer),
                Column('minutes', Integer),
                Column('time', Integer),
                Column('project', String),
                Column('work', String),
                )
metadata.create_all(engine)
conn = engine.connect()
