from flask import Flask, render_template, request, session, redirect, url_for, flash, render_template_string
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'EXPLANASENAIADM'

# Função para verificar se o arquivo é permitido

# página inicial onde é carregada as postagens existentes
@app.route("/", methods=['GET', 'POST']) # cria a rota e os métodos de pegar e postar
def home(): # define a rota
    return render_template('home.html') # carrega o html do código

# página onde o usuário pode ver as suas postagens
@app.route('/postagens', methods=['GET','POST'])
def postagens():
    nomeUsuario = session.get('nomeUsuario')
    session['nomeUsuario'] = nomeUsuario
    if session['nomeUsuario'] == None: # caso a sessão esteja vazia (sem o nome de usuário)
        return render_template_string("""
            <h2>Olá! Por favor faça seu <a href="{{url_for('login')}}">login</a> ou <a href="{{url_for('cadastro')}}">cadastre-se</a> no site</h2>
        """)
    else:
        return render_template('postagens.html')

# página onde pessoas podem postar suas ofertas, vendas ou doações
@app.route('/ofertas')
def ofertas():
    return render_template('ofertas.html')

# página onde é feito o login
@app.route('/login', methods=['GET', 'POST'])
def login():
    nomeUsuario = request.form.get('nomeUsuario') # pega as informações do front (nome de usuário e senha)
    senha = request.form.get('senha')
    con = sql.connect('banco.db') # se conecta ao banco
    cur = con.cursor()
    cur.execute('select * from usuarios') # seleciona todos os usuários
    usuariosBD = cur.fetchall() # coloca em uma variável
    cont = 0 # um contador que será utilizado para verificar o id do usuário (posição dele)
    for usuario in usuariosBD: # para cada usuário existente
        usuarioNome = str(usuario[1]) # usuario[1] é o nome de usuário, pois o usuario[0] é o ID
        usuarioSenha = str(usuario[3])
        if nomeUsuario == usuarioNome and senha == usuarioSenha: # se as informações forem iguais
            # o usuário entrará no site
            session['nomeUsuario'] = request.form.get('nomeUsuario')
            return redirect(url_for('home'))
        if cont >= len(usuariosBD): # caso as informações não forem iguais, ou seja, não tiver um usuário com as informações equivalentes
            return redirect(url_for('login')) # o usuário retornará para a página de login
    con.close()
    return render_template('login.html')

# página onde é feito o cadastro
@app.route('/cadastro', methods=['GET','POST'])
def cadastro():
    if request.method == 'POST':
        # ele vai pegar a informação do cadastro
        nomeUsuario = request.form.get('nomeUsuario')
        nomeCompleto = request.form.get('nomeCompleto')
        senha = request.form.get('senha')
        fotoPerfil = request.form.get('fotoPerfil')
        # vai se conectar ao banco
        con = sql.connect('banco.db')
        cur = con.cursor()
        # caso o nome de usuário que a pessoa colocou não exista ainda:
        try:
            # vai inserir as informações no banco de dados
            cur.execute('insert into usuarios (NOME_USUARIO,NOME_COMPLETO,SENHA) values(?,?,?)', (nomeUsuario,nomeCompleto,senha))
            con.commit()
            con.close() # e depois fechá-lo
        # caso o nome de usuário já exista no banco:
        except:
            flash('Cadastro inválido') # vai aparecer que o cadastro foi inválido
            return redirect(url_for('cadastro')) # e vai atualizar a página
        # caso dê tudo certo no cadastro:
        session['nomeUsuario'] = request.form.get('nomeUsuario') # a sessão da pessoa será seu nome de usuário, porque ele é único
        return redirect(url_for('home')) # vai redirecionar para a página principal
    return render_template('cadastro.html')


# página que quando o usuário apertar em sair irá redirecionar para o login
@app.route('/sair')
def sair():
    session.pop('nomeUsuario', default=None) # a sessão será fechada
    return redirect(url_for('login')) # vai voltar para a página de login
    return render_template('login.html')

# página onde o usuário poderá postar as reportagens
@app.route('/postar')
def postar():
    nomeUsuario = session.get('nomeUsuario')
    session['nomeUsuario'] = nomeUsuario
    if session['nomeUsuario'] == None: # caso a sessão esteja vazia (sem o nome de usuário)
        return render_template_string("""
            <h2>Olá! Por favor faça seu <a href="{{url_for('login')}}">login</a> ou <a href="{{url_for('cadastro')}}">cadastre-se</a> no site</h2>
        """)
        return redirect(url_for('home'))
    else:
        return render_template('postar.html')

# roda o código
if __name__ == '__main__':
    app.run(debug=True)