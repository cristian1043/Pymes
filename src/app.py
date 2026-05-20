from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# =====================================
# CONEXION MYSQL
# =====================================

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="facturacionpymes"
)

cursor = conexion.cursor(dictionary=True)
app = Flask(__name__)

#inicio de la aplicacion

@app.route("/")
def index():
    return render_template("index.html")

#Ruta de clientes

@app.route("/Nuevo_Clientes")
def Nuevo_Clientes():
    return render_template("NuevoClientes.html")

@app.route("/Ver_Clientes")
def Ver_Clientes():
    return render_template("VerClientes.html")

#Ruta de productos

@app.route("/Nuevo_Producto", methods=["POST"])
def Nuevo_Productos():
    return render_template("NuevoProducto.html")
    
    nombre = request.form["nombre"]
    precio = request.form["precio"]
    stock = request.form["stock"]

    # GENERAR CODIGO AUTOMATICO
    cursor.execute("SELECT COUNT(*) total FROM productos")

    resultado = cursor.fetchone()

    numero = resultado["total"] + 1

    codigo = f"P{numero:03}"

    sql = """
        INSERT INTO productos(nombre, precio, stock, codigo)
        VALUES(%s,%s,%s,%s)
    """

    valores = (nombre, precio, stock, codigo)

    cursor.execute(sql, valores)

    conexion.commit()

    return redirect("/Ver_Producto")
    
@app.route("/Ver_Producto")
def Ver_Productos():
    
    cursor.execute("SELECT * FROM productos")
    
    productos = cursor.fetchall()
    
    return render_template(
        "VerProducto.html", 
        productos=productos
    )

#Ruta de facturas

@app.route("/Nueva_Factura")
def Nueva_Factura():
    return render_template("NuevaFactura.html")

@app.route("/Ver_Factura")
def Ver_Facturas():
    return render_template("VerFactura.html")

@app.route("/Detalle_Factura")
def Detalle_Factura():
    return render_template("DetalleFactura.html")

#Ruta Reportes

@app.route("/Reporte_Clientes")
def Reporte_Clientes():
    return render_template("ReporteClientes.html")

@app.route("/Reporte_Ventas")
def Reporte_Ventas():
    return render_template("ReporteVentas.html")



if __name__ == '__main__':
    app.run(debug=True)
    
