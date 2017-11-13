
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

waho = Restaurant(name = "WaHo")
session.add(waho)
session.commit()
# session.query(Restaurant).all()

# aaaaaa
