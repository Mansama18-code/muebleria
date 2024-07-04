# Instalar con pip install Flask
from flask import Flask, request, jsonify

# Instalar con pip install flask-cors
from flask_cors import CORS

# Instalar con pip install mysql-connector-python
import mysql.connector

# Si es necesario, pip install Werkzeug
from werkzeug.utils import secure_filename

# No es necesario instalar, es parte del sistema standard de Python
import os
import time

app = Flask(__name__)
CORS(app)  # Esto habilitará CORS para todas las rutas

'''Trabajo Backend Python 
EXITO-MUEBLE'''
# Definimos una lista de diccionarios para guardar los muebles
# Campos de la tabla mueble:
#  cod_articulo nombre descripcion material cantidad preciomin preciomay 


class Mueble:
    def __init__(self, host, user, password, database):
        
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )
        self.cursor = self.conn.cursor()

        # Intentamos seleccionar la base de datos
        try:
            self.cursor.execute(f"USE {database}")
        except mysql.connector.Error as err:
            # Si la base de datos no existe, la creamos
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:# type: ignore
                self.cursor.execute(f"CREATE DATABASE {database}")
                self.conn.database = database # type: ignore
            else:
                raise err

        self.cursor = self.conn.cursor(dictionary=True)
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mueble (
            cod_articulo INT AUTO_INCREMENT PRIMARY KEY,
            nombre VARCHAR(20) NOT NULL,
            descripcion VARCHAR(30) NOT NULL,
            material VARCHAR(20) NOT NULL,
            cantidad INT NOT NULL,
            preciomin DECIMAL(10, 2) NOT NULL,
            preciomy DECIMAL(10, 2) NOT NULL
            )''')
        self.conn.commit()
        self.cursor.close()
        self.cursor = self.conn.cursor(dictionary=True)

    # Agregar un mueble (create)
    def agregar_mueble(self, nombre, descripcion, material, cantidad, preciomin, preciomay):
        
        sql = "INSERT INTO mueble (nombre, descripcion, material, cantidad, preciomin, preciomay) VALUES (%s, %s, %s, %s, %s, %s)"
        valores = (nombre, descripcion, material, cantidad, preciomin, preciomay)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.lastrowid
    
    def consultar_mueble(self, cod_articulo):
        # Consultamos un producto a partir de su código
        self.cursor.execute(f"SELECT * FROM mueble WHERE cod_articulo = {cod_articulo}")
        return self.cursor.fetchone()

    def mostrar_producto(self, codigo):
        # Mostramos los datos de un producto a partir de su código
        producto = self.consultar_mueble(codigo)

        if producto:
            print("-" * 40)
            print(f"Código.....: {producto['cod_articulo']}")# type: ignore
            print(f"Nombre.....: {producto['nombre']}")# type: ignore
            print(f"Descripción: {producto['descripcion']}")# type: ignore
            print(f"Material ..: {producto['material']}")# type: ignore
            print(f"Cantidad...: {producto['cantidad']}")# type: ignore
            print(f"Precio Minorista.....: {producto['preciomin']}")# type: ignore
            print(f"Precio Mayorista.....: {producto['preciomay']}") # type: ignore
            
            print("-" * 40)
        else:
            print("Producto no encontrado.")
        
    def modificar_producto(self, nuevo_nombre, nueva_descripcion, nuevo_material, nueva_cantidad, nuevo_preciomin, nuevo_preciomay, cod_articulo):
        sql = "UPDATE mueble SET nombre=%s,  descripcion = %s, material = %s, cantidad = %s, preciomin = %s, preciomay = %s  WHERE cod_articulo = %s"
        valores = ( nuevo_nombre, nueva_descripcion, nuevo_material, nueva_cantidad, nuevo_preciomin, nuevo_preciomay, cod_articulo)
        self.cursor.execute(sql, valores)
        self.conn.commit()
        return self.cursor.rowcount > 0

    # Eliminar un mueble
    def eliminar_mueble (self, codigo):
        # Eliminamos un mueble de la tabla a partir de su código
        self.cursor.execute(f"DELETE FROM mueble WHERE cod_articulo = {codigo}")
        self.conn.commit()
        return self.cursor.rowcount > 0

    def listar_productos(self):
        self.cursor.execute("SELECT * FROM mueble")
        mueble = self.cursor.fetchall()
        return mueble    


# ############################################    
#       Programa              principal      #
# ############################################

mueble1= Mueble(host='localhost', user='root', password='', database='muebles')

# Agregamos productos a la tabla mueble
#mueble1.agregar_mueble('Mesa', 'ovalada', 'Granito' , 30 , 33500 , 30000)  

''''
x
print(mueble1.consultar_mueble(int(1)))

# Consultamos un producto y lo mostramos
cod_prod = int(input("Ingrese el código del producto: "))
producto = mueble1.consultar_mueble(cod_prod)
print(producto)
if producto:
     print(f"Producto encontrado: {producto['cod_articulo']} - {producto['descripcion']}")
else:
     print(f'Producto {cod_prod} no encontrado.')

print(mueble1.listar_productos())
'''

'''# Modificar y consultar producto
mueble1.mostrar_producto(3)

mueble1.modificar_producto ('Estanteria', 'pequeña', 'aluminio' , 10 , 15000 , 12000, 3)
mueble1.mostrar_producto(3)
'''

'''# Eliminamos un producto
mueble1.eliminar_mueble(2)
productos = mueble1.listar_productos()
for producto in productos:
    print(producto)'''


@app.route("/mueble", methods=["GET"])
def listar_productos():
        muebles = mueble1.listar_productos()
        
        return jsonify(muebles)


#--------------------------------------------------------------------
# Agregar un producto
#--------------------------------------------------------------------
@app.route("/mueble", methods=["POST"])
#La ruta Flask `/productos` con el método HTTP POST está diseñada para 
# permitir la adición de un nuevo producto a la base de datos.
#La función agregar_producto se asocia con esta URL y es llamada cuando
#se hace una solicitud POST a /productos.
def agregar_producto():
#Recojo los datos del form
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    material = request.form['material']
    cantidad = request.form['cantidad']
    preciomn = request.form['preciomn']
    preciomy = request.form['preciomy']
    
    nuevo_codigo = mueble1.agregar_mueble(nombre, descripcion, material, cantidad, preciomn, preciomy)
    if nuevo_codigo:

    #Si el producto se agrega con éxito, se devuelve una respuesta
    #JSON con un mensaje de éxito y un código de estado HTTP 201 (Creado).
        return jsonify({"mensaje": "Producto agregado correctamente.", "codigo": nuevo_codigo}), 201
    else:
        #Si el producto no se puede agregar, se devuelve una respuesta JSON con un mensaje de error y un código de estado HTTP 500 (Internal Server Error).
        return jsonify({"mensaje": "Error al agregar el producto."}), 500

#--------------------------------------------------------------------

#--------------------------------------------------------------------
# Modificar un producto según su código
#--------------------------------------------------------------------
@app.route("/mueble/<int:codigo>", methods=["PUT"])
#La ruta Flask /productos/<int:codigo> con el método HTTP PUT está
#diseñada para actualizar la información de un producto existente en la
#base de datos, identificado por su código.
#La función modificar_producto se asocia con esta URL y es invocada
#cuando se realiza una solicitud PUT a /productos/ seguido de un número
#(el código del producto).
def modificar_producto(codigo):
#Se recuperan los nuevos datos del formulario
        nueva_nombre = request.form.get("nombre")     
        nueva_descripcion = request.form.get("descripcion")
        nueva_material = request.form.get("material")
        nueva_cantidad = request.form.get("cantidad")
        nuevo_preciomin = request.form.get("precio")
        nuevo_preciomay = request.form.get("proveedor")


        # Se llama al método modificar_producto pasando el codigo del
        #producto y los nuevos datos.
        if mueble1.modificar_producto(nueva_nombre, nueva_descripcion, nueva_material, nueva_cantidad, nuevo_preciomin,nuevo_preciomay, codigo ):
        #Si la actualización es exitosa, se devuelve una respuesta JSON
        #con un mensaje de éxito y un código de estado HTTP 200 (OK).
            return jsonify({"mensaje": "Producto modificado"}), 200
        else:
            #Si el producto no se encuentra (por ejemplo, si no hay ningún
            #producto con el código dado), se devuelve un mensaje de error con un
            #código de estado HTTP 404 (No Encontrado).
            return jsonify({"mensaje": "Producto no encontrado"}), 403
#--------------------------------------------------------------------
# Eliminar un producto según su código
#--------------------------------------------------------------------
def eliminar_producto(codigo):
# Busco el producto en la base de datos
    producto = mueble1.consultar_mueble(codigo)
    if producto: # Si el producto existe, verifica si hay una imagen asociada en el servidor.
            # Armo la ruta a la imagen
            #ruta_imagen = os.path.join(ruta_destino, producto["imagen_url"])
            # Y si existe, la elimina del sistema de archivos.
            #if os.path.exists(ruta_imagen):
                #os.remove(ruta_imagen)
            # Luego, elimina el producto del catálogo
            if mueble1.eliminar_mueble(codigo):
    #Si el producto se elimina correctamente, se devuelve una
    #respuesta JSON con un mensaje de éxito y un código de estado HTTP 200 (OK).

                return jsonify({"mensaje": "Producto eliminado"}), 200
            else:
            #Si ocurre un error durante la eliminación (por ejemplo, si
            #el producto no se puede eliminar de la base de datos por alguna razón),
            #se devuelve un mensaje de error con un código de estado HTTP 500 (Error
            #Interno del Servidor).

                return jsonify({"mensaje": "Error al eliminar el producto"}), 500
    else:
        #Si el producto no se encuentra (por ejemplo, si no existe un
        #producto con el codigo proporcionado), se devuelve un mensaje de error
        #con un código de estado HTTP 404 (No Encontrado).
        return jsonify({"mensaje": "Producto no encontrado"}), 404

if __name__ == "__main__":
   app.run(debug=True)