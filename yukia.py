from sqlalchemy import create_engine
engine = create_engine('postgresql://inyuki_yukia:7cd26db5@localhost/inyuki_yukia', echo=True)

result = engine.execute('''DROP TABLE units''')
result = engine.execute('''CREATE TABLE units (id serial, unit varchar(40) NOT NULL);''')
result = engine.execute('''INSERT INTO units VALUES (1, 'Bricks laid');''')
result = engine.execute('''SELECT * FROM units;''')

for row in result:
    print "unit:", row['unit']

result = engine.execute('''DROP TABLE units;''')
result.close()

