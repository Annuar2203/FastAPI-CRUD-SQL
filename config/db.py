from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://name:password@localhost:port/name_database")

# Para realizar la conexion de manera correcta se hace lo siguiente
# usuario: se coloca el usuario en donde se encuentra la base de datos, MySQL lo suele colocar de manera determinada como root
# password: La contraseña del usuario en donde se encuentra la base de datos
# Port: El puerto donde se encuentra el usuario
# name_database: El nombre de la base de datos


metadata = MetaData()
