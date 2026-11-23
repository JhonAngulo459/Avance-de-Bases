from pymongo import MongoClient
import certifi

MONGO_URI ="mongodb+srv://jhonangulo_db_user:uENv1BJaL4eojvuk@cluster0.udqz71b.mongodb.net/"
ca = certifi.where()

def dbConnection():
    try:
        client = MongoClient(MONGO_URI, tlsCAFile=ca)
        db = client["dbb_products_app"]
    except ConnectionError:
        print("Error de conexión con la base de datos")
    return db