# -*- coding: utf-8 -*-
import pymysql 
pymysql.install_as_MySQLdb()
import MySQLdb


class Database(object):
    con = None # Conexão com o banco
    c = None # Cursor

    def __init__(self):
        # Cria primeira conexão
        if(Database.con is None):
            Database.con = MySQLdb.connect(host='db',user='root', passwd='pass_here', db='teste')
            Database.c = Database.con.cursor()

    # Método utilizado sempre que for inserir no Banco
    @staticmethod
    def insert (query):
        Database()
        Database.c.execute(query)
        return Database.c.fetchall() # Converte todas as linhas retornadas para uma matriz

    # Método utilizado sempre que for consultar no Banco
    @staticmethod
    def get (query):
        Database()
        Database.c.execute(query)
        return Database.c.fetchall() # Converte todas as linhas retornadas para uma matriz

    # Método utilizado para deletar algum elemento do banco
    @staticmethod
    def delete (query):
        Database()
        Database.c.execute(query)
        return Database.c.fetchall() # Converte todas as linhas retornadas para uma matriz

    # Método utilizado para atualizar o banco
    @staticmethod
    def update (query):
        Database()
        Database.c.execute(query)
        Database.con.commit()
        return Database.c.fetchall() # Converte todas as linhas retornadas para uma matriz


    # Método utilizado para realizar outras tarefas no BD, como criar uma tabela
    @staticmethod
    def query (query):
        Database()
        Database.c.execute(query)
        return Database.c.fetchall() # Converte todas as linhas retornadas para uma matriz
