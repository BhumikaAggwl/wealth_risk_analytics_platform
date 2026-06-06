from sqlalchemy import create_engine

USERNAME = "root"
PASSWORD = "rj20cf0362"
HOST = "localhost"
DATABASE = "wealth_platform"

engine = create_engine(
    f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}/{DATABASE}"
)

try:
    connection = engine.connect()
    print("Database Connected Successfully!")
    connection.close()

except Exception as e:
    print("Connection Failed")
    print(e)