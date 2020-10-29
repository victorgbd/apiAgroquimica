from flask import Flask, request, redirect, url_for, send_from_directory
import json
import os
from werkzeug.utils import secure_filename
import mysql.connector
from PIL import Image
# from predict import IA
from Data.user_model import user_model_from_dict
from Data.user_model import user_model_to_dict
from Data.user_model import UserModelElement

from Data.usere_model import user_e_model_from_dict
from Data.usere_model import user_e_model_to_dict
from Data.usere_model import UserEModelElement

from Data.detallefact_model import detallefact_model_from_dict
from Data.detallefact_model import detallefact_model_to_dict
from Data.detallefact_model import DetallefactModelElement

from Data.factura_model import factura_model_from_dict
from Data.factura_model import factura_model_to_dict
from Data.factura_model import FacturaModelElement

upload_folder = os.path.abspath("./Fotos/")
extenciones_permitidas = {'png', 'jpg', 'jpeg', 'gif'}


def verifica(filename):
    try:
        im = Image.open(filename)
        return True
    except IOError:
        return False


def permitidas(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in extenciones_permitidas


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config["UPLOAD_FOLDER"] = upload_folder
# redn = IA()

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="agroquimica"
)
bdcursor = mydb.cursor()


# @app.route("/upload", methods=["GET", "POST"])
# def upload_file():
#     try:
#         if request.method == "POST":
#             f = request.files["file"]
#             filename = secure_filename(f.filename)
#             if filename == '':
#                 return "Sube algun archivo"
#             if f and permitidas(filename):
#                 f.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
#                 print(f)
#                 print(filename)
#                 if verifica(upload_folder+'/'+filename):
#                     prediccion = redn.predict(upload_folder+'/'+filename)
#                     os.remove(upload_folder+'/'+filename)
#                     return prediccion
#                 os.remove(upload_folder+'/'+filename)
#             return "archivo no permitido"
#     except IOError:
#         return "ui un erroi en el archivo"

#     return """<!DOCTYPE html>
# <html>
# <head>
#     <meta charset="utf-8">
#     <title>Upload File</title>
# </head>
# <body>
#     <h1>Upload File</h1>
#     <form method="POST" enctype="multipart/form-data">
#         <input type="file" name="file">
#         <input type="submit" value="Upload">
#     </form>
# </body>
# </html>"""

@app.route('/users', methods=['POST', 'GET','PUT'])
def users():
    if request.method == 'POST':
        us = user_model_from_dict(json.loads(request.get_data()))
        query = "INSERT INTO `usuario`(`nickname`, `contrasena`, `tipoacceso`) VALUES ('{}', '{}','{}');".format(
            us[0].nickname, us[0].contrasena,us[0].tipoacceso)
        bdcursor.execute(query)
        mydb.commit()
        print(bdcursor.rowcount, "record inserted.")
        return json.dumps("Usuario Insertado correctamente")
    elif request.method == 'PUT':
        us = user_model_from_dict(json.loads(request.get_data()))
        query = "UPDATE `usuario` SET `nickname`='{}',`contrasena`='{}',`tipoacceso`='{}' WHERE `codusuario`='{}';".format(
            us[0].nickname, us[0].contrasena, us[0].tipoacceso,us[0].codusuario)
        bdcursor.execute(query)
        mydb.commit()
        print(bdcursor.rowcount, "record updated.")
        return json.dumps("Usuario Actualizado correctamente")
    else:
        us = user_model_from_dict(json.loads(request.get_data()))
        bdcursor.execute("SELECT * FROM usuario Where `nickname`='{}' and `contrasena`='{}'".format(us[0].nickname,us[0].contrasena))
        myresult = bdcursor.fetchall()
        list_users = []
        for x in myresult:
            us = UserModelElement(x[0], x[1], x[2],x[3])
            list_users.append(us)
        return json.dumps(user_model_to_dict(list_users))
@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        us = user_model_from_dict(json.loads(request.get_data()))
        if(us[0].codusuario==1):
            bdcursor.execute("SELECT * FROM usuario Where `nickname`='{}' and `contrasena`='{}'".format(us[0].nickname,us[0].contrasena))
            myresult = bdcursor.fetchall()
            list_users = []
            for x in myresult:
                us = UserModelElement(x[0], x[1], x[2],x[3])
                list_users.append(us)
            return json.dumps(user_model_to_dict(list_users))
        else:
            bdcursor.execute("SELECT * FROM usuario Where `nickname`='{}'".format(us[0].nickname))
            myresult = bdcursor.fetchall()
            list_users = []
            for x in myresult:
                us = UserModelElement(x[0], x[1], x[2],x[3])
                list_users.append(us)
            return json.dumps(user_model_to_dict(list_users))
    else:
        email  = request.args.get('email', None)
        password  = request.args.get('password', None)
        bdcursor.execute("SELECT p.nombre,p.apellido,c.correo,u.contrasena,dir.region,dir.Provincia,dir.municipio,dir.sector,dir.Calle"+
        ",dir.referencia,d.tipo,d.numeracion,tel.numero FROM cliente as c INNER JOIN persona as p on c.codper = p.codper "+
        "INNER JOIN ver_direccion as dir on p.coddir = dir.Codigo INNER JOIN usuario as u "+
        "on c.codusuario = u.codusuario inner join documento as d on p.coddocu=d.coddocu "+
        "inner join telefono as tel on c.codtel=tel.codtel WHERE c.correo = '{}' AND u.contrasena='{}'".format(email,password))
        myresult = bdcursor.fetchall()
        list_users = []
        print(myresult)
        for x in myresult:
            us = UserEModelElement(x[0], x[1], x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12])
            list_users.append(us)
        return json.dumps(user_e_model_to_dict(list_users))



@app.route('/factura', methods=['POST', 'PUT'])
def factura():
    if request.method == 'POST':
        det = factura_model_from_dict(json.loads(request.get_data()))
        bdcursor.callproc('sp_factura',[det[0].codcli, det[0].estado, det[0].tipfac, det[0].codemp, det[0].balance,det[0].total])
        mydb.commit()
        myresult=[]
        for result in bdcursor.stored_results():
            myresult=result.fetchall()
        print(myresult[0][0])
        print(bdcursor.rowcount, "record inserted.")
        return json.dumps(myresult[0][0])

@app.route('/factura/<int:id>', methods=['GET','DELETE'])
def factura_by_id(id):
    if request.method == 'GET':
        bdcursor.execute("SELECT * FROM factura where numfact={}".format(id))
        myresult = bdcursor.fetchall()
        list_dtf = []
        for x in myresult:
            print(x)
            dtf = FacturaModelElement(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
            list_dtf.append(dtf)
        return json.dumps(factura_model_to_dict(list_dtf))
    return json.dumps("Metodo no creado")

@app.route('/dfactura', methods=['POST', 'PUT', 'GET'])
def detallefacturas():
    if request.method == 'POST':
        det = detallefact_model_from_dict(json.loads(request.get_data()))
        for x in det:
            bdcursor.callproc('sp_detallefactura',[x.numfac, x.codproducto, x.cantvent, x.precvent, x.coduni])
        mydb.commit()
        print(bdcursor.rowcount, "record inserted.")
        return json.dumps("Detalle de factura almacenado correctamente")
        
@app.route('/dfactura/<int:id>', methods=['GET','DELETE'])
def detallefactura(id):
    if request.method == 'GET':
        bdcursor.execute("SELECT * FROM detalle_factura where numfact={}".format(id))
        myresult = bdcursor.fetchall()
        list_dtf = []
        for x in myresult:
            dtf = DetallefactModelElement(x[0],x[1],x[2],x[3],x[4])
            list_dtf.append(dtf)
        return json.dumps(detallefact_model_to_dict(list_dtf))
    return json.dumps("Metodo no creado")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
