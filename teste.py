import mysql.connector
from mysql.connector import Error
from faker import Faker
import datetime
import random

fake = Faker('pt_BR')

def generate_random_birthdate(start_age=18, end_age=90):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=end_age*365)
    end_date = today - datetime.timedelta(days=start_age*365)
    return fake.date_between_dates(date_start=start_date, date_end=end_date)

def generate_fake_price(min_price=10, max_price=1000, decimal_places=2):
    return round(random.uniform(min_price, max_price), decimal_places)

def idioma_aleatorio():
    idiomas = ['Inglês', 'Mandarim', 'Espanhol', 'Hindi', 'Francês']
    return random.choice(idiomas)

def insert_data(query, values):
    try:
        con = mysql.connector.connect(host='localhost', database='db_livraria', user='root', password='93893415')
        cursor = con.cursor()
        cursor.execute(query, values)
        con.commit()
        print(cursor.rowcount, "registros inseridos na tabela")
    except Error as erro:
        print(f'Falha ao inserir dados no MySQL: {erro}')
    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print('Conexão finalizada')

def insert_autores():
    quantidade = 100
    autores = [fake.name() for _ in range(quantidade)]
    for id, autor in enumerate(autores, 1):
        query = """INSERT INTO Autor (cod_autor, nome, data_nasc, pais_nasc, biografia)
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (id, autor, generate_random_birthdate(), fake.country(), fake.text())
        insert_data(query, values)

def insert_livros():
    quantidade = 400
    livros = [fake['pt-BR'].sentence(nb_words=3, variable_nb_words=True) for _ in range(quantidade)]
    for id, livro in enumerate(livros, 1):
        query = """INSERT INTO Livro (cod_livro, nome, lingua, ano)
                   VALUES (%s, %s, %s, %s)"""
        values = (id, livro, idioma_aleatorio(), fake.date_time().year)
        insert_data(query, values)

def insert_autores_livros():
    quantidade = 400
    for id in range(quantidade):
        query = """INSERT INTO Autor_has_livro (cod_autor, cod_livro)
                   VALUES (%s, %s)"""
        values = (random.randint(1, 100), id + 1)
        insert_data(query, values)

def insert_editoras():
    quantidade = 50
    for id in range(quantidade):
        query = """INSERT INTO Editora (cod_editora, nome, endereco, telefone)
                   VALUES (%s, %s, %s, %s)"""
        values = (id + 1, fake.company(), fake.address(), fake.phone_number())
        insert_data(query, values)

def insert_edicoes():
    quantidade = 1000
    contador_livros = 1
    for id in range(quantidade):
        query = """INSERT INTO Edicao (cod_isbn, preco, ano, num_pag, qtde_estoque, cod_livro, cod_editora)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        if contador_livros > 40:
            contador_livros = 1
        values = (fake.isbn10(), generate_fake_price(), fake.date_time().year, random.randint(50, 300),
                  random.randint(1, 60), contador_livros, random.randint(1, 50))
        contador_livros += 1
        insert_data(query, values)



def select_consulta1(consulta):
    try:
        con = mysql.connector.connect(host='localhost', database='db_livraria', user='root', password='93893415')
        cursor = con.cursor()
        cursor.execute(consulta)
        linhas = cursor.fetchall()
        print(f"Numero total de resgistros retornados: {cursor.rowcount}")
        
        print("\n os nomes de todos os autores que têm edições de seus livros publicados com uma determinada editora\n")
        for linha in linhas:
            print(f"Nome: {linha[0]}")
        cursor.close()
    except Error as erro:
        print(f'Falha ao inserir dadso no MySQL {erro}')

    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print('Conexao finalizada')

def select_consulta2(consulta):
    try:
        con = mysql.connector.connect(host='localhost', database='db_livraria', user='root', password='93893415')
        cursor = con.cursor()
        cursor.execute(consulta)
        linhas = cursor.fetchall()
        print(f"Numero total de resgistros retornados: {cursor.rowcount}")
        
        print("\n informações das edições que tenha a palavra dada no título do livro da edição\n")
        for linha in linhas:
            print(f"Numero_Edicao: {linha[0]}")
            print(f"Editora: {linha[1]}")
            print(f"Titulo_Livro: {linha[2]}")
            print(f"Primeiro_Autor: {linha[3]}")
        cursor.close()

    except Error as erro:
        print(f'Falha ao inserir dadso no MySQL {erro}')

    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print('Conexao finalizada')

def select_consulta3(consulta):
    try:
        con = mysql.connector.connect(host='localhost', database='db_livraria', user='root', password='93893415')
        cursor = con.cursor()
        cursor.execute(consulta)
        linhas = cursor.fetchall()
        print(f"Numero total de resgistros retornados: {cursor.rowcount}")
        
        print("as informações das edições onde a string fornecida esteja presente no nome de pelo menos um dos autores dos livros")
        for linha in linhas:
            print(f"Id_Edicao: {linha[0]}")
            print(f"Nome_Editora: {linha[1]}")
            print(f"Livro Titulo: {linha[2]}")
        cursor.close()
    except Error as erro:
        print(f'Falha ao inserir dadso no MySQL {erro}')

    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print('Conexao finalizada')

def updateBanco(alteracao):
    try:
        con = mysql.connector.connect(host='localhost', database='db_livraria', user='root', password='93893415')
        cursor = con.cursor()
        cursor.execute(alteracao)
        con.commit()
        print("UPDATE REALIZADO COM SUCESSO")
    except Error as erro:
        print(f'Falha ao inserir dadso no MySQL {erro}')

    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print('Conexao finalizada')

def insert_bd(novo_isbn, novo_preco, novo_ano, novo_num_pag, nova_qtde_estoque, codigo_livro_existente, codigo_editora_anterior):
    try:
        con = mysql.connector.connect(host='localhost', database='db_livraria', user='root', password='93893415')
        inserir_edicao = f"""INSERT INTO Edicao (cod_isbn, preco, ano, num_pag, qtde_estoque, cod_livro, cod_editora)
                                VALUES ('{novo_isbn}', '{novo_preco}', '{novo_ano}', '{novo_num_pag}', '{nova_qtde_estoque}', '{codigo_livro_existente}', '{codigo_editora_anterior}')
                        """

        cursor = con.cursor()
        cursor.execute(inserir_edicao)
        con.commit()
        print(cursor.rowcount, "Nova edicao inserido na tabela")
        cursor.close()

    except Error as erro:
        print(f'Falha ao inserir dadso no MySQL {erro}')

    finally:
        if con.is_connected():
            cursor.close()
            con.close()
            print('Conexao finalizada')




if __name__ == "__main__":
   
  # insert_autores()
  # insert_livros()
  # insert_autores_livros()
  # insert_editoras()
  # insert_edicoes()

    ###CONSULTAS###
   # cod_editora = int(int(input('Digite o codigo da editora: ')))
   # consulta1 = f""" 
   #                 SELECT DISTINCT Autor.nome
   #                 FROM Autor
   #                 JOIN Autor_has_Livro ON Autor.cod_autor = Autor_has_Livro.cod_autor
   #                 JOIN Livro ON Autor_has_Livro.cod_livro = Livro.cod_livro
   #                JOIN Edicao ON Livro.cod_livro = Edicao.cod_livro
   #                JOIN Editora ON Edicao.cod_editora = Editora.cod_editora
   #                 WHERE Editora.cod_editora = '{cod_editora}'
   #                """
   # select_consulta1(consulta1)
    
   # palavra1 = input('Escreva uma palavra para efetuar a consulta: ')
   # consulta2 = f"""
   #                SELECT Edicao.cod_isbn AS Numero_Edicao, Editora.nome AS Nome_Editora, Livro.nome AS Titutlo_livro, Autor.nome AS Primeiro_Autor
   #                 FROM Edicao
   #                 JOIN Livro ON Edicao.cod_livro = Livro.cod_livro
   #                 JOIN Autor_has_Livro ON Livro.cod_livro = Autor_has_Livro.cod_livro
   #                 JOIN Autor ON Autor_has_Livro.cod_autor = Autor.cod_autor
   #                 JOIN Editora ON Edicao.cod_editora = Editora.cod_editora
   #                 WHERE Livro.nome LIKE '%{palavra1}%' 
   #                 ORDER BY Edicao.cod_isbn;
   #                """
   # select_consulta2(consulta2)


   # palavra2 = input('Escreva um nome para efetuar a consulta: ')
   # consulta3 = f""" 
   #                 SELECT DISTINCT Edicao.cod_isbn AS Id_Edicao, Editora.nome AS Nome_Editora, Livro.nome AS Titulo_Livro
   #                 FROM Edicao
   #                 JOIN Livro ON Edicao.cod_livro = Livro.cod_livro
   #                 JOIN Autor_has_Livro ON Livro.cod_livro = Autor_has_Livro.cod_livro
   #                 JOIN Autor ON Autor_has_Livro.cod_autor = Autor.cod_autor
   #                 JOIN Editora ON Edicao.cod_editora = Editora.cod_editora
   #                 WHERE Autor.nome LIKE '%{palavra2}%'
   #                """
   # select_consulta3(consulta3)


    ###UPDATE###
   # nome_editora = input('Digite o nome da editora para receber o aumento de 20%: ')
   # updateBanco(f"""
   #             UPDATE Edicao
   #             JOIN Livro ON Edicao.cod_livro = Livro.cod_livro
   #             JOIN Editora ON Edicao.cod_editora = Editora.cod_editora
   #             SET Edicao.qtde_estoque = Edicao.qtde_estoque * 1.2
   #             WHERE Editora.nome = '{nome_editora}'
   #             """)


    ###INSERT####
    novo_isbn = input('Digite o novo ISBN: ')
    novo_preco = float(input('Digite o novo preco: '))
    novo_ano = input('Digite o novo ano: ')
    novo_num_pag = int(input('digite o numero de paginas: '))
    novo_qtd_estoque = int(input('digite a quantidade de estoque: '))
    codigo_livro_exist = int(input('digite o codigo do livro existente:  '))
    codigo_editora_anterior = int(input('digite o codigo da editora anterior: '))
    insert_bd(novo_isbn, novo_preco, novo_ano, novo_num_pag, novo_qtd_estoque, codigo_livro_exist, codigo_editora_anterior)