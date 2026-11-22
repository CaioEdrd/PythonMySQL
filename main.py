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
        #comando para limpar a tabela
        cursor.execute(
                f"""
                TRUNCATE TABLE customers

            """
        )
        connection.commit()
    with connection.cursor() as cursor:
        cursor.execute(
                f"""
                INSERT INTO customers
                (nome,idade)
                VALUES
                ("Caio", 23)
                """
        )
        connection.commit()
    print(cursor)

# #sem context manager
# cursor = connection.cursor()
# cursor.close()
# connection.close()