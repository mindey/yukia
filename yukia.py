from sqlalchemy import create_engine
engine = create_engine('postgresql://inyuki_yukia:7cd26db5@localhost/inyuki_yukia', echo=True)
from sqlalchemy import MetaData
meta_data = MetaData()
from sqlalchemy import Table, Column, Integer, String, ForeignKey

units_table = Table('units', meta_data,
    Column('id', Integer, primary_key=True),
    Column('unit', String(40)),
)

meta_data.create_all(engine)

class Unit(object):
    def __init__(self, unit):
        self.unit = unit

    def __repr__(self):
        return "" % (self.unit,)

from sqlalchemy.orm import mapper, relation, backref
mapper(Unit, units_table)

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

brick = Unit('bricks laid')
tile = Unit('roof tiles mounted')
units_list = [brick, tile]
session.add_all(units_list)
session.commit()

for u in units_list:
    print "Unit:\t", u.unit

