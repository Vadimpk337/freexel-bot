from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy import  Column, String, Integer, BigInteger
 
engine = create_engine(f"postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_IP}/{settings.DB_NAME}")

Base = declarative_base()
class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String(50))
	telegram_id = Column(BigInteger, index=True)
	status = Column(String(10), default='Гость')

	search_count = Column(Integer, default=0)

	phone_try_search = Column(Integer, default=0)
	iin_try_search = Column(Integer, default=0)


class Searcher(Base):
	__tablename__ = 'searcher'

	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	telegram_id = Column(BigInteger, index=True)
	wh_phone_search = Column(String(16), default=None)
	wh_command_search = Column(String(50), default=None) 


class Uncap(Base):
	__tablename__ = 'uncap'

	id = Column(Integer, primary_key=True)
	name = Column(String(50), default=None)
	phone = Column(String(16))
	city = Column(String(30), default=None)
	email = Column(String(40), default=None)
	birthday = Column(String(20))

class Operator(Base):
	__tablename__ = 'operator'

	id = Column(Integer, primary_key=True)
	name = Column(String(20), default=None)
	code = Column(String(6))

class Scammer(Base):
	__tablename__ = 'scammer'

	id = Column(Integer, primary_key=True)
	group = Column(String(50), default=None)
	phone = Column(String(16))
		

Base.metadata.create_all(bind=engine)
 
