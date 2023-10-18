from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
import os

#Conexão com o banco de dados
def get_db_conexao():
    db_path = os.path.join(app.root_path, 'dados.db')
    conexao = sql.connect(db_path)
    conexao.row_factory = sql.Row
    return conexao

def iniciar_db():
    conexao = get_db_conexao()
    with app.open_resource('esquema.sql', mode='r') as comandos:
        conexao.cursor().executescript(comandos.read())
    conexao.commit()
    conexao.close()

app = Flask(__name__)
app.secret_key = 'meublogotavio'
logado = False
usuario = 'admin'
senha = '1234'

if session:
    session.clear()

# Rota da página inicial
@app.route("/")
def index():
    global logado
    iniciar_db()
    conexao = get_db_conexao()
    posts = conexao.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    conexao.close()
    
    if 'login' in session and session['login']: #Confirma se o indíce existe
        logado = True
    else:
        logado = False
    
    titulo = 'PÁGINA INICIAL'
    return render_template('index.html', titulo=titulo, posts=posts, logado=logado)



@app.route('/modelo')
def modelo():
    titulo = 'PÁGINA MODELO'
    return render_template('modelo.html', titulo=titulo)

@app.route('/postar')
def novopost():
    titulo = 'NOVO POST'
    return render_template('postar.html', titulo=titulo)

@app.route('/login')
def login():
    titulo = 'LOGIN'
    return render_template('login.html', titulo=titulo)

#ROTA PARA RECEBER A POSTAGEM DO FORMULÁRIO
@app.route('/cadpost', methods=['POST'])
def cadpost():
    titulo = request.form['titulo']
    conteudo = request.form['conteudo']
    conexao = get_db_conexao()
    conexao.execute('INSERT INTO posts (titulo, conteudo) VALUES (?,?)', (titulo, conteudo))
    conexao.commit()
    conexao.close()
    return redirect('/')

@app.route('/excluir/<id>')
def excluir(id):
    conexao = get_db_conexao()
    conexao.execute('DELETE FROM posts WHERE id = ?',(id))
    conexao.commit()
    conexao.close()
    return redirect('/')

@app.route('/entrar', methods=['POST'])
def entrar():
    global usuario, senha, logado

    usuario_enter = request.form['nome']
    senha_enter = request.form['senha']

    if usuario_enter == usuario and senha_enter == senha:
        session['login'] = True
        return redirect('/')
    else: 
        return render_template('login.html', msg="Usuário/Senha incorretos!")
    
@app.route('/logoff')
def logoff():
    session['login'] = False
    return redirect('/')

app.run(debug=True) #debug = True coloca o servidor em modo de teste