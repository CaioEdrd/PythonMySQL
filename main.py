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
        # cursor.execute(
        #         f"""
        #         TRUNCATE TABLE customers

        #     """
        # )
        # connection.commit()
        #insert com placeholder para evitar sqlinjection
    with connection.cursor() as cursor:
        #comando sql com valores sendo placeholders
        sql = f"""
                INSERT INTO customers
                (nome,idade)
                VALUES
                (%s, %s)
                """
        data = ("João",25)
        cursor.execute( sql, data )
        connection.commit()

    with connection.cursor() as cursor:
        #comando sql com valores sendo placeholders
        sql = f"""
                INSERT INTO customers
                (nome,idade)
                VALUES
                (%(nomePessoa)s, %(idadePessoa)s)
                """
        data = {
            "nomePessoa": "Allana",
            "idadePessoa": 22
        }
        cursor.execute( sql, data )
        connection.commit()
    print(cursor)

# #sem context manager
# cursor = connection.cursor()
# cursor.close()
# connection.close()