from fastapi import APIRouter, Response, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED
from schema.user_schema import UserSchema, DataUser
from config.db import engine
from model.users import users
from werkzeug.security import generate_password_hash, check_password_hash


user = APIRouter()

@user.get('/')
def root():
    return {"message" : "Hi I am FastAPI with a router"}

@user.get('/api/user')
def get_users():
    with engine.connect() as conn:
        result = conn.execute(users.select()).fetchall()

        # Obtener los nombres de las columnas
        columns = users.columns.keys()

        # Convertir el resultado a una lista de diccionarios
        user_list = [dict(zip(columns, row)) for row in result]

        return user_list

@user.get('/api/user/{user_id}', response_model=UserSchema)
def get_user(user_id: int):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.id == user_id)).first()

        if result is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Obtener los nombres de las columnas
        columns = users.columns.keys()

        # Crear un diccionario combinando nombres de columnas y valores de la fila
        user_dict = dict(zip(columns, result))

        # Convertir 'id' a cadena (str) si existe
        if 'id' in user_dict:
            user_dict['id'] = str(user_dict['id'])

        # Crear una instancia de UserSchema a partir del diccionario
        return UserSchema(**user_dict)

@user.post('/api/user', status_code=HTTP_201_CREATED)
def create_user(data_user: UserSchema):
    with engine.connect() as conn:
        new_user = data_user.dict()
        new_user["user_passw"] = generate_password_hash(data_user.user_passw, "pbkdf2:sha256:30", 30)
        conn.execute(users.insert().values(new_user))
        conn.commit()
        return Response(status_code=HTTP_201_CREATED)


@user.post('/api/user/login', status_code=200)
def user_login(data_user: DataUser):
    with engine.connect() as conn:
        result = conn.execute(users.select().where(users.c.username == data_user.username)).first()
        if result != None:
            check_passw = check_password_hash(result[3], data_user.user_passw)
            if check_passw:
                return {
                    "status" : 200,
                    "message" : "Access successfully"
                }
            else:
                return {
                    "status" : 200,
                    "message" : "Access denied"
                }
        return {
            "status" : HTTP_401_UNAUTHORIZED,
            "message" : "Access denied"
        }




@user.put('/api/user/{user_id}', response_model=UserSchema)
def update_user(data_update: UserSchema, user_id: int):
    with engine.connect() as conn:
        encryp_passw = generate_password_hash(data_update.user_passw, "pbkdf2:sha256:30", 30)

        # Verificar que el usuario exista antes de la actualización
        existing_user = conn.execute(users.select().where(users.c.id == user_id)).first()
        if existing_user is None:
            raise HTTPException(status_code=404, detail="User not found")

        # Actualizar la base de datos y obtener el número de filas afectadas
        update_query = (
            users.update()
                .values(name=data_update.name, username=data_update.username, user_passw=encryp_passw)
                .where(users.c.id == user_id)
        )

        conn.execute(update_query)

        # result = conn.execute(update_query)
        # affected_rows = result.rowcount

        # if affected_rows == 0:
        #     # Si no se afectaron filas, lanzar un error
        #     raise HTTPException(status_code=404, detail="User not found or no changes were made")

        # Confirmar la transacción
        conn.commit()

        # Seleccionar y devolver el usuario actualizado como un diccionario
        result = conn.execute(users.select().where(users.c.id == user_id)).first()

        # Obtener los nombres de las columnas
        columns = users.columns.keys()

        # Crear un diccionario combinando nombres de columnas y valores de la fila
        user_dict = dict(zip(columns, result))

        # Convertir 'id' a cadena (str) si existe
        if 'id' in user_dict:
            user_dict['id'] = str(user_dict['id'])

        # Aplicar el modelo UserSchema al diccionario convertido
        return UserSchema(**user_dict)
    

@user.delete('/api/user/{user_id}', status_code=HTTP_204_NO_CONTENT)
def delete_user(user_id:int):
    with engine.connect() as conn:
        conn.execute(users.delete().where(users.c.id == user_id))

        conn.commit()

        return Response(status_code=HTTP_204_NO_CONTENT)