from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:22032004@localhost:3306/databasepython")



metadata = MetaData()