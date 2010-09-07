from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, sessionmaker

Base = declarative_base()

class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Stock(%r)" % (self.name)

class Name(Base):
    __tablename__ = 'names'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Name(%r)" % (self.name)

class Label(Base):
    __tablename__ = 'labels'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Label(%r)" % (self.name)

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    named_by = Column(Integer, ForeignKey('names.id'))
    stocked_at = Column(Integer, ForeignKey('stocks.id'))
    labeled_with = Column(Integer, ForeignKey('labels.id'))

    name = relation("Name", backref='items', lazy=False)
    stock = relation("Stock", backref='items', lazy=False)
    label = relation("Label", backref='items', lazy=False)

    def __init__(self):
        pass
    def __repr__(self):
        return "Item(%r, %r, %r)" % (self.name, self.stock, self.label)

class Process(Base):
    __tablename__ = 'processes'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    owned_by = Column(Integer, ForeignKey('items.id'))

    item = relation("Item", backref='processes', lazy=False)

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Process(%r, %r)" % (self.name, self.item)

class Unit(Base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    owned_by = Column(Integer, ForeignKey('processes.id'))

    process = relation("Process", backref='units', lazy=False)

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "Unit(%r, %r)" % (self.name, self.process)

engine = create_engine('postgresql://inyuki_yukia:7cd26db5@localhost/inyuki_yukia', echo=False)
Base.metadata.create_all(engine)
