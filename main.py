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
        #comando sql com valores sendo passado via dicionário
        sql = f"""
                INSERT INTO customers
                (nome,idade)
                VALUES
                (%(nomePessoa)s, %(idadePessoa)s)
                """
        data = {
            "nomePessoa": "Pedro",
            "idadePessoa": 22
        }
        cursor.execute( sql, data )
        connection.commit()
    with connection.cursor() as cursor:
        #Passando vários valores em um insert
        sql = f"""
                INSERT INTO customers
                (nome,idade)
                VALUES
                (%(nomePessoa)s, %(idadePessoa)s)
                """
       #os dados são dicionários dentro de uma tupla
        data = (
            {"nomePessoa": "Allana","idadePessoa": 22},
            {"nomePessoa": "Pablo","idadePessoa": 27},
            {"nomePessoa": "Joana","idadePessoa": 28}    
        )
        #troca o comando execute por executemany
        cursor.executemany( sql, data )
        connection.commit()

#Ler valores do Banco de Dados

    with connection.cursor() as cursor:
        #select todas as colunas
        sql = f"""
                SELECT * FROM customers
                """
        cursor.execute( sql )

        #utilizar o fetchall/fetchmany/fetchone
        dataSelect1 = cursor.fetchall()
        #sempre que usar fetchall deve fazer o for na tupla gerada
        for row in dataSelect1:
            print(row)

    with connection.cursor() as cursor:
        #select dos dados com id maior que 2
        sql = f"""
                SELECT * 
                FROM customers
                WHERE id > 2
                """
        cursor.execute( sql )

        dataSelect1 = cursor.fetchall()
        for row in dataSelect1:
            print(row)

    with connection.cursor() as cursor:
        nomeUsuario = input("Digite seu nome: ")
        #select com base no nome, sempre que pedir um valor do usuário utilizar o placeholder
        sql = f"""
                SELECT idade
                FROM customers
                WHERE nome = %s 
                """
        cursor.execute(sql,(nomeUsuario,))
        #fetchone pega a primeira ocorrência
        dataSelect1 = cursor.fetchone()
        print(f"Sua idade é: {dataSelect1}")


    with connection.cursor() as cursor:
        #ao pedir ID converte para int
        menorID = input(int("Digite menor ID: "))
        maioID = input(int("Digite maior ID: "))
        #utilizando o between para pegar o nome entre os valores de ID passado
        sql = f"""
                SELECT nome
                FROM customers
                WHERE 
                ID BETWEEN %s AND %s 
                """
        cursor.execute(sql,(menorID, maioID))

        dataSelect1 = cursor.fetchall()
        for row in dataSelect1:
            print(row)        
    print(cursor)

# #sem context manager
# cursor = connection.cursor()
# cursor.close()
# connection.close()