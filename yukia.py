from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker
from time import time

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Stock(%r)" % (self.name)

class Type(Base):                      # Generalizations for names. I.e., Sandwitch, Eggs.
    __tablename__ = 'types'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Type(%r)" % (self.name)

class Name(Base):                      # Particular names, i.e., "McChicken"
    __tablename__ = 'names'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, unique=True)

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Name(%r)" % (self.name)
    # So, an item name is fully specified by Type and Name, i.e., [Sandwitch][McChiken]


class Label(Base):      # To be used to sort Items into "Producers", "Raw Materials", "Currencies" and other functional kinds.
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, unique=True)

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Label(%r)" % (self.name)

class Quant(Base):             # Smallest Unit for counting Items,   
    __tablename__ = 'quants'   # i.e., Quant of [Milk "Milkyway"] = 0.5 liter pack 
                               # i.e., Quant of [Orange Juice "Slee"] = 0.5 liter pack
    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Quant(%r, %r)" % (self.name)

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    typed_as = Column(Integer, ForeignKey('types.id'), nullable=False)  # i.e., "Sandwitch"
    named_by = Column(Integer, ForeignKey('names.id'), nullable=True)  # i.e., "McChicken"
    stocked_at = Column(Integer, ForeignKey('stocks.id'), nullable=False)   # i.e., London, New York
    labeled_with = Column(Integer, ForeignKey('labels.id'), nullable=False) # i.e., Producer, Raw material, Currency
    quantized_by = Column(Integer, ForeignKey('quants.id'), nullable=False) # i.e., 0.5 liter pack 

    type = relation("Type", backref='types', lazy=False)
    name = relation("Name", backref='items', lazy=False)
    stock = relation("Stock", backref='items', lazy=False)
    label = relation("Label", backref='items', lazy=False)
    quant = relation("Quant", backref='quants', lazy=False)

    def __init__(self):
        pass
    def __repr__(self):
        return "Item(%r, %r, %r, %r, %r)" % (self.type, self.name, self.stock, self.label, self.quant)

class Process(Base):
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    owned_by = Column(Integer, ForeignKey('items.id'))

    item = relation("Item", backref='processes', lazy=False)

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Process(%r, %r)" % (self.name, self.item)

class Unit(Base):                            # For measuring Performances of each Process
    __tablename__ = 'units'                  # Each Process should have a unique set of Units 

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False)
    owned_by = Column(Integer, ForeignKey('processes.id'))

    process = relation("Process", backref='units', lazy=False)

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Unit(%r, %r)" % (self.name, self.process)

class Performance(Base):
    __tablename__ = 'performances'

    id = Column(Integer, primary_key=True)                  
    hour = Column(Integer, unique=True)                    # Unique hour since 1/1/1970. 
    total = Column(Integer)                                # Total production amount in the hour. 
    owned_by = Column(Integer, ForeignKey('processes.id')) # The process measured.
    measured_by = Column(Integer, ForeignKey('units.id'))  # The measurement units.

    process = relation("Process", backref='performances', lazy=False)
    unit = relation("Unit", backref='units', lazy=False)

    def __init__(self, hour=0, total=0):
        self.hour = int(time.time())/3600 # As perofrmance is measured, the hour id is calculated.
        self.total = total
    def __repr__(self):
        return "Performance(%r, %r, %r)" % (self.total, self.process, self.unit)
    # The object(s) should be written to database and recreated if the hour doesn't match the current one.
    # No need for frequent cron jobs, because the time when the object was created is memorized.
    # One cron job in the end of the working day is sufficient to include the last hour data of the day.

class Market(Base):
    __tablename__ = 'markets'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), nullable=False, unique=True)

    def __init__(self, name='Home'):
        self.name = name
    def __repr__(self):
        return "Market(%r)" % (self.name)

class Source(Base):      # Prototype for issuing Items.
    __tablename__ = 'sources'

    id = Column(Integer, primary_key=True)
    typed_as = Column(Integer, ForeignKey('types.id'), nullable=False)  # i.e., "Sandwitch"
    named_by = Column(Integer, ForeignKey('names.id'), nullable=True)  # i.e., "McChicken"
    marketed_in = Column(Integer, ForeignKey('markets.id')) # Thought: MarketID = 1 -> Home 
    labeled_with = Column(Integer, ForeignKey('labels.id'), nullable=False) # i.e., Producer, Raw material, Currency
    quantized_by = Column(Integer, ForeignKey('quants.id'), nullable=False) # i.e., 0.5 liter pack 

    type = relation("Type", backref='types', lazy=False)
    name = relation("Name", backref='items', lazy=False)
    market = relation("Market", backref='sources', lazy=False)
    label = relation("Label", backref='items', lazy=False)
    quant = relation("Quant", backref='quants', lazy=False)
 
    def __init__(self, name='Home'):
        pass 
    def __repr__(self):
        return "Source(%r, %r, %r, %r, %r)" % (self.type, self.name, self.market, self.label, self.quant) 

#class Exchange(Base):
#    __tablename__ = 'exchanges'
#
#    id = Column(Integer, primary_key=True)
#    exchanged_for = Column(Dictionary)  # i.e. {Item1: Quantity1, Item2 : Quantity2, ...}  (labeled as currency)
#    exchanged_into = Column(Dictionary) # i.e. {Source1: Quantity1, Source2: Quantity2, ...}

#class Transaction(Base):
#    __tablename__ = 'transactions'
#
#    id = Column(Integer, primary_key=True)
#    time = Column(Float)
#    content = Column(Set)               # i.e. [exchange1, exchange2,...] 


engine = create_engine('sqlite:///yukia.db', echo=False)
Base.metadata.create_all(engine)
