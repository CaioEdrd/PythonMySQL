import pymysql, dotenv, os

dotenv.load_dotenv()

connection = pymysql.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
)
#com context manager
with connection:
    with connection.cursor() as cursor:
        #comandos SQL
        cursor.execute(
            f"""
                CREATE TABLE IF NOT EXISTS customers
                (id INT NOT NULL AUTO_INCREMENT,
                nome VARCHAR(50) NOT NULL,
                idade INT NOT NULL,
                PRIMARY KEY (id)
                )
            """
        )
        connection.commit()

        print(cursor)

# #sem context manager
# cursor = connection.cursor()
# cursor.close()
# connection.close()