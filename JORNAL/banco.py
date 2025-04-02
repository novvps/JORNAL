import sqlite3 as sql

con = sql.connect('banco.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS usuarios')

comando = '''CREATE TABLE "usuarios" (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        NOME_USUARIO VARCHAR(200) UNIQUE NOT NULL,
        NOME_COMPLETO VARCHAR(250) NOT NULL,
        SENHA VARCHAR(200) NOT NULL
        )'''

cur.execute(comando)
con.commit()
con.close()

con = sql.connect('banco.db')
cur = con.cursor()
cur.execute('DROP TABLE IF EXISTS postagem')

comando = '''CREATE TABLE "postagem" (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER NOT NULL,
        titulo TEXT NOT NULL,
        conteudo TEXT NOT NULL,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        imagem BLOB NOT NULL,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (ID)
        )'''

cur.execute(comando)
con.commit()
con.close()



