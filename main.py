import pymysql, dotenv, os

dotenv.load_dotenv()

connection = pymysql.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USER'],
    password=os.environ['MYSQL_PASSWORD'],
    database=os.environ['MYSQL_DATABASE'],
    cursorclass=pymysql.cursors.DictCursor, #altera o cursor tradicional que é tupla para dicionário
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
        # for row in dataSelect1:
        #     print(row)

    with connection.cursor() as cursor:
        # nomeUsuario = input("Digite seu nome: ")
        #select com base no nome, sempre que pedir um valor do usuário utilizar o placeholder
        sql = f"""
                SELECT idade
                FROM customers
                WHERE nome = %s 
                """
        # cursor.execute(sql,(nomeUsuario,))
        # #fetchone pega a primeira ocorrência
        # dataSelect1 = cursor.fetchone()
        # print(f"Sua idade é: {dataSelect1}")


    with connection.cursor() as cursor:
        #ao pedir ID converte para int
        # menorID = input(int("Digite menor ID: "))
        # maioID = input(int("Digite maior ID: "))
        # #utilizando o between para pegar o nome entre os valores de ID passado
        sql = f"""
                SELECT nome
                FROM customers
                WHERE 
                ID BETWEEN %s AND %s 
                """
        # cursor.execute(sql,(menorID, maioID))

        # dataSelect1 = cursor.fetchall()
        # for row in dataSelect1:
        #     print(row)       
    
#Apagar valores
    with connection.cursor() as cursor:
        sql = f"""
                DELETE FROM customers
                WHERE ID = 4
                """
        cursor.execute( sql )
        
        cursor.execute('SELECT * FROM customers')
    # print('-'*10, 'DELETE ID 4', '-'*10)
    # for row in cursor.fetchall():
    #     print(row)
    #     connection.commit()

#Atualizando valores
    with connection.cursor() as cursor:
        sql = f"""
                UPDATE customers
                SET
                nome = %s, idade = %s
                WHERE ID = 1
                """
        cursor.execute( sql, ("Caio",33) )
        connection.commit()

    #     cursor.execute('SELECT * FROM customers')
    # print('-'*10, 'UPDATE ID 1', '-'*10)
    # for row in cursor.fetchall():
    #     print(row)

#utilizando fetchall sem colocar o valor em uma variável e utilizar o scroll do cursor
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM customers')
    # print('-'*10, 'FOR 1', '-'*10)
    # for row in cursor.fetchall():
    #     print(row)
    # print('-'*10, 'FOR 2', '-'*10)
    # cursor.scroll(-2) #aqui faz o cursor "rolar" dentro dos parenteses posso colocar a quantidade de linhas para voltar ou avançar se modo relativo (padrão)
    # for row in cursor.fetchall():
    #     print(row)
    # print('-'*10, 'FOR 3', '-'*10)
    # cursor.scroll(0,'absolute') #o modo absoluto permite coocar a linha que quer que ele vá diretamente
    # for row in cursor.fetchall():
    #     print(row)

# #sem context manager
# cursor = connection.cursor()
# cursor.close()
# connection.close()