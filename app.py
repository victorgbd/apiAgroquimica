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

from Data.productos_model import productos_model_from_dict
from Data.productos_model import productos_model_to_dict
from Data.productos_model import ProductosModelElement

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

@app.route('/user', methods=['POST', 'GET','PUT'])
def user():
    if request.method == 'PUT':
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
    elif request.method == 'POST':
        det = user_e_model_from_dict(json.loads(request.get_data()))
        bdcursor.callproc('sp_createusere',[det[0].nombre,det[0].apellido,det[0].correo,det[0].contrasena,
        det[0].codciudad,det[0].codpais,det[0].direccion,det[0].tipo,det[0].numeracion,det[0].numerotelf])
        mydb.commit()
        return json.dumps("usuario insertado correctamente")
    else:
        email  = request.args.get('email', None)
        password  = request.args.get('password', None)
        bdcursor.execute("SELECT p.nombre,p.apellido,c.codclie,c.correo,u.contrasena,pais.codpais,pais.descripcion "+
        "as pais,ciu.codprovi,ciu.descripcion as ciudad,dir.coddir,dir.Descripcion as direccion,"
        +"d.tipo,d.numeracion,tel.numero FROM cliente as c INNER JOIN persona as p on c.codper = p.codper"+
        " INNER JOIN direccion as dir on p.coddir = dir.coddir INNER JOIN pais on dir.codpais = pais.codpais"+
        " INNER JOIN provincia as ciu on dir.codciudad =ciu.codprovi INNER JOIN usuario as u "+
        "on c.codusuario = u.codusuario inner join documento as d on p.coddocu=d.coddocu inner join "+
        "telefono as tel on c.codtel=tel.codtel WHERE c.correo = '{}' AND u.contrasena='{}'".format(email,password))
        myresult = bdcursor.fetchall()
        list_users = []
        print(myresult)
        for x in myresult:
            us = UserEModelElement(x[0], x[1], x[2],x[3],x[4],x[5],x[6],x[7],x[8],x[9],x[10],x[11],x[12],x[13])
            list_users.append(us)
        return json.dumps(user_e_model_to_dict(list_users))

@app.route('/direccion', methods=['GET'])
def direccion():
    codpais  = request.args.get('codpais', None)
    codprovincia  = request.args.get('codprovincia', None)
    coddir = request.args.get('coddireccion', None)
    if(codpais is None and codprovincia is None and coddir is None):
        bdcursor.execute("SELECT * FROM pais")
        myresult = bdcursor.fetchall()
        list_region = []
        for x in myresult:
            us = {"cod":x[0],"descripcion":x[1]}
            list_region.append(us)
        return json.dumps(list_region)
    elif(codpais is not None):
        bdcursor.execute("SELECT * FROM provincia where codpais={}".format(codpais))
        myresult = bdcursor.fetchall()
        list_provin = []
        for x in myresult:
            us = {"cod":x[0],"descripcion":x[1]}
            list_provin.append(us)
        return json.dumps(list_provin)
    elif(coddir is not None):
        bdcursor.execute("SELECT descripcion,codciudad,codpais FROM direccion where coddir={}".format(coddir))
        myresult = bdcursor.fetchall()
        list_provin = []
        for x in myresult:
            us = {"descripcion":x[0],"codciudad":x[1],"codpais":x[2]}
            list_provin.append(us)
        return json.dumps(list_provin)
    



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

# @app.route('/factura/<int:id>', methods=['GET','DELETE'])
# def factura_by_id(id):
#     if request.method == 'GET':
#         bdcursor.execute("SELECT * FROM factura where numfact={}".format(id))
#         myresult = bdcursor.fetchall()
#         list_dtf = []
#         for x in myresult:
#             print(x)
#             dtf = FacturaModelElement(x[0],x[1],x[2],x[3],x[4],x[5],x[6],x[7])
#             list_dtf.append(dtf)
#         return json.dumps(factura_model_to_dict(list_dtf))
#     return json.dumps("Metodo no creado")

@app.route('/dfactura', methods=['POST', 'PUT', 'GET'])
def detallefacturas():
    if request.method == 'POST':
        det = detallefact_model_from_dict(json.loads(request.get_data()))
        for x in det:
            bdcursor.callproc('sp_detallefactura',[x.numfac, x.codproducto, x.cantvent, x.precvent, x.coduni])
        mydb.commit()
        print(bdcursor.rowcount, "record inserted.")
        return json.dumps("Detalle de factura almacenado correctamente")
        
# @app.route('/dfactura/<int:id>', methods=['GET','DELETE'])
# def detallefactura(id):
#     if request.method == 'GET':
#         bdcursor.execute("SELECT * FROM detalle_factura where numfact={}".format(id))
#         myresult = bdcursor.fetchall()
#         list_dtf = []
#         for x in myresult:
#             dtf = DetallefactModelElement(x[0],x[1],x[2],x[3],x[4])
#             list_dtf.append(dtf)
#         return json.dumps(detallefact_model_to_dict(list_dtf))
#     return json.dumps("Metodo no creado")

@app.route('/productos', methods=['GET'])
def productos():
    if request.method == 'GET':
        bdcursor.execute("SELECT prod.codproducto,prod.descripcion,"+
        "vsu.coduni,u.descripcion,vsu.cantext,vsu.precioventa,"+
        "tip.codtipopro,tip.descripcion,prod.url_image FROM producto as prod "+
        "INNER join tipo_de_producto as tip on prod.tipoprod = "+
        "tip.codtipopro INNER JOIN productovsunidad as vsu on "+
        "prod.codproducto=vsu.codproducto INNER JOIN unidad as u on "+
        "vsu.coduni=u.coduni")
        myresult = bdcursor.fetchall()
        list_dtf = []
        for x in myresult:
            dtf = ProductosModelElement(str(x[0]),x[1],str(x[2]),x[3],str(x[4]),str(x[5]),str(x[6]),x[7],x[8])
            list_dtf.append(dtf)
        return json.dumps(productos_model_to_dict(list_dtf))
    return json.dumps("Metodo no creado")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
