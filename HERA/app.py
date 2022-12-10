from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_session import Session
from cs50 import SQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message

import time, datetime, serial, csv

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

#Configuracion de email
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = 'herabpmdatos@gmail.com'
app.config["MAIL_PASSWORD"] = 'sumjkajlqlgmmrtu'
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = '1234'
Session(app)



db = SQL("sqlite:///DatosHera.db")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route('/registro', methods=['GET','POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        edad = request.form.get('edad')
        usuario = request.form.get('usuario')
        correo = request.form.get('correo')
        clave = request.form.get('clave')
        confirmacion = request.form.get('confirmacion')
        
        if not nombre:
            flash("Ingrese su nombre")
            return render_template("registro.html", alert = "Ingrese su nombre") 
        
        if not edad:
            return render_template("registro.html", alert = "Ingrese su edad") 
        
        if not usuario:
            return render_template("registro.html", alert = "Ingrese un usuario")
        
        if not correo:
            return render_template("registro.html", alert = "Ingrese un correo")
        
        if not clave:
            return render_template("registro.html", alert = "Ingrese una contraseña")
        
        if not confirmacion:
            return render_template("registro.html", alert = "Repita la contraseña")

        if clave != confirmacion:
            return render_template("registro.html", alert = "Las claves no coinciden")

        clave_cifrada = generate_password_hash(clave)
        
        try:
            id = db.execute("INSERT INTO usuarios(NombreCompleto, Edad, Usuario, Correo, Clave) \
                    VALUES (?, ?, ?, ?, ?)", nombre, int(edad), usuario, correo, clave_cifrada)

            msg = Message('Gracias por tu registro, lo haz hecho correctamente!', 
                        sender = app.config["MAIL_USERNAME"], recipients=[correo])

            msg.html = render_template('registroEmail.html', nombre=nombre)
            mail.send(msg)

            session["id_usuario"] = id

            return render_template("index.html", success = "Se ha registrado correctamente")
        
        except:
            return render_template("registro.html", alert = "Revise sus datos")
    
    else:
        return render_template('registro.html')

@app.route('/logout')
def logout():
	session['id_usuario'] = None

	return redirect(url_for('index'))

@app.route('/login', methods=['GET','POST'])
def login():
    session.clear()
    if request.method == "POST":
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")

        if not usuario:
            flash("Ingresa un usuario")
            return redirect("/login")
        if not clave:
            flash("Ingresa una clave")
            return redirect("/login")
        
        rows = db.execute("SELECT * FROM usuarios WHERE Usuario = ?", request.form.get("usuario"))
        

        if len(rows) != 1 or not check_password_hash(rows[0]["Clave"], request.form.get("clave")):
            return render_template("login.html",alert = "Revise sus datos")

        session["id_usuario"] = rows[0]["id"]

        return render_template("index.html",success="Ha iniciado sesion")

    else:
        return render_template("login.html")

@app.route("/medicionbase", methods=["GET", "POST"])
def medicionbase():
    if session['id_usuario'] == None:
        return redirect('/login')
    if request.method == "POST":
        return redirect(url_for('medicion'))
    else:
        return render_template('medicionbase.html')

@app.route("/medicion", methods=["GET", "POST"])
def medicion():
    if session['id_usuario'] == None:
        return redirect('/login')
    if request.method == "GET":
        usuario_id = session['id_usuario']
        a=0.0
        b=0.0
        c=0.0
        i=0.0
        a=time.time()
        serialArduino = serial.Serial("COM4", 115200)
        time.sleep(2)
        lista = []
        lista_aux = []
        sum = 0
        promedio = 0
        fecha = datetime.datetime.now()
        while i < 30:
            bpm = serialArduino.readline().decode('ascii')
            bpm = int(bpm.replace("\r\n",""))
            lista.append(bpm)
            b=time.time()
            c=b-a
            if c>=1.0:
                a=time.time()
                i=i+1
                print(i)
            else:
                continue
            for j in lista:
                if j > 50 and j < 100:
                    lista_aux.append(j)
                    sum += j
                else:
                    continue

        try:            
            promedio =  int(sum/len(lista_aux))
            print(promedio)
            # Insertar en la base de datos
            db.execute("INSERT INTO datos (usuario_id, Bpm, Fecha) \
                    VALUES (?, ?, ?)", usuario_id, promedio, fecha)
            print(lista_aux)
            print(f"BPM = {promedio}")
            
            #Enviar mensaje de medicion al usuario
            nombre = db.execute("SELECT NombreCompleto FROM usuarios WHERE id = :id", id=usuario_id)[0]["NombreCompleto"]
            correo = db.execute("SELECT Correo FROM usuarios WHERE id = :id", id=usuario_id)[0]["Correo"]
            
            msg = Message('Haz obtenido una nueva medición!', 
                        sender = app.config["MAIL_USERNAME"], recipients=[correo])

            msg.html = render_template('medicionEmail.html', nombre=nombre, promedio=promedio)
            mail.send(msg)
        except:
            return render_template("medicionbase.html", alert = "Ha ocurrido un error, vuelva a intentarlo")

        return render_template("medicion.html", success = "Ha obtenido una nueva medición", promedio=promedio)
    else:
        return redirect("/")

@app.route("/historial")
def historial():
    usuario_id = session['id_usuario']
    historial = db.execute("SELECT * FROM usuarios JOIN datos ON id = usuario_id WHERE usuario_id = :id", id=usuario_id)
    return render_template("historial.html", datos=historial)

@app.route("/tutorial", methods=["GET", "POST"])
def tutorial():
    return render_template("tutorial.html")

@app.route("/loginAdmin", methods=["GET", "POST"])
def loginAdmin():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        clave = request.form.get("clave")

        # if usuario == "admin" and clave == "adminHERA0119":
        #     return redirect(url_for("index"))

        datos = db.execute("SELECT * FROM usuario_admin WHERE usuario = ?", usuario)[0]

        if clave == datos["clave"]:
            session["id_usuario"] = datos["id"]
            return redirect(url_for("panelAdmin"))
        
        if (datos is None):
            return render_template("loginAdmin.html", alert ="Error: El usuario no existe")
        
        return render_template("panelAdmin.html", success ="Ha iniciado sesion como administrador")

    else:
        return render_template("loginAdmin.html")

@app.route("/panelAdmin", methods=["GET", "POST"])
def panelAdmin():
    if request.method == "POST":
        return render_template("index.html")
    else:
        return render_template("panelAdmin.html")

@app.route("/usuarios")
def usuarios():
    usuarios = db.execute("SELECT * FROM usuarios")
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/datos")
def datos():
    datos = db.execute("SELECT * FROM usuarios JOIN datos ON id = usuario_id ORDER BY usuario ASC")
    return render_template("datos.html", datos=datos)

@app.route("/descarga")
def descarga():
    datos = db.execute("SELECT NombreCompleto, Edad, Usuario, Correo, Bpm, Fecha FROM usuarios JOIN datos ON id = usuario_id ORDER BY NombreCompleto")
    
    with open("datos.csv", "w", newline='') as archivo:
        w = csv.DictWriter(archivo, datos[0].keys())
        w.writeheader()
        for i in datos:
            w.writerow(i)

    return send_file("datos.csv", as_attachment=True)

if __name__ =='__main__':
    app.run(debug = True)