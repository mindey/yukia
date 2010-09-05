from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapper, relation, backref
from sqlalchemy.orm import sessionmaker
engine = create_engine('postgresql://inyuki_yukia:7cd26db5@localhost/inyuki_yukia', echo=False, useexisting=True)
meta_data = MetaData()

# Creating database model

stocks_table = Table('stocks', meta_data,
    Column('sid', Integer, primary_key=True),
    Column('name', String(30)),
)

names_table = Table('names', meta_data,
    Column('nid', Integer, primary_key=True),
    Column('name', String(40)),
)

items_table = Table('items', meta_data,
    Column('iid', Integer, primary_key=True),         # item id (unique)
    Column('nid', Integer, ForeignKey('names.nid')),  # name id
    Column('sid', Integer, ForeignKey('stock.sid')),  # stock id
    Column('lid', Integer, ForeignKey('labels.lid')), # label id
) 

labels_table = Table('labels', meta_data,
    Column('lid', Integer, primary_key=True),
    Column('name', String(30)),
)

processes_table = Table('items', meta_data,
    Column('pid', Integer, primary_key=True),
    Column('name', String(40)),
    Column('item', Integer, ForeignKey('items.iid')), # producer id ( a kind of label for process )
)

meta_data.create_all(engine)

# Creating and mapping OO model to the database model

#class Unit(object):
#    def __init__(self, unit):
#        self.unit = unit
#
#    def __repr__(self):
#        return "" % (self.unit,)

#mapper(Unit, units_table)

# Creating and adding some objects to the database 
#Session = sessionmaker(bind=engine)
#session = Session()

#brick = Unit('bricks laid')
#tile = Unit('roof tiles mounted')
#units_list = [brick, tile]

#session.add_all(units_list)
#session.commit()

# Querying the database (should be)


# Printing some ojbects from the database (should be) 
#for u in units_list:
#    print "Unit:\t", u.unit

