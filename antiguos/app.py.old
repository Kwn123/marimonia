from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///catalogo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

UPLOAD_FOLDER = "static/images"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


db = SQLAlchemy(app)


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), unique=True, nullable=False)

    productos = db.relationship(
        "Producto",
        backref="categoria",
        lazy=True
    )


class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(200))

    categoria_id = db.Column(
        db.Integer,
        db.ForeignKey("categoria.id"),
        nullable=False
    )


@app.route("/")
def inicio():

    categorias = Categoria.query.all()
    productos = Producto.query.all()

    return render_template(
        "index.html",
        categorias=categorias,
        productos=productos
    )


@app.route("/admin")
def admin():

    categorias = Categoria.query.all()
    productos = Producto.query.all()

    return render_template(
        "admin.html",
        categorias=categorias,
        productos=productos
    )


@app.route("/admin/producto", methods=["POST"])
def agregar_producto():

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    categoria_id = request.form["categoria"]

    imagen = request.files["imagen"]

    nombre_imagen = ""
    
   if imagen and imagen.filename:
      nombre_imagen = imagen.filename

    ruta = os.path.join(
        app.config["UPLOAD_FOLDER"],
        nombre_imagen
    )

    imagen.save(ruta)


    producto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        imagen=nombre_imagen,
        categoria_id=categoria_id
    )


    db.session.add(producto)
    db.session.commit()


    return redirect(url_for("admin"))


def crear_base():

    db.create_all()

    if Categoria.query.count() == 0:

        categorias = [
            "Cerámica",
            "Velas",
            "Cemento",
            "Sahumerios",
            "Porta sahumerios",
            "Esencias"
        ]

        for nombre in categorias:
            db.session.add(
                Categoria(nombre=nombre)
            )

        db.session.commit()

@app.route("/categoria/<nombre>")
def categoria(nombre):

    categoria = Categoria.query.filter_by(
        nombre=nombre
    ).first()

    if categoria:

        productos = Producto.query.filter_by(
            categoria_id=categoria.id
        ).all()

        return render_template(
            "categoria.html",
            categoria=categoria,
            productos=productos
        )

    return "Categoría no encontrada"

if __name__ == "__main__":

    with app.app_context():
        crear_base()


    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
