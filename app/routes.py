import os

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    url_for,
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from werkzeug.security import check_password_hash, generate_password_hash

from .models import db, Categoria, Producto, Usuario

main = Blueprint("main", __name__)


# ==========================
# Inicio
# ==========================

@main.route("/")
def inicio():

    categorias = Categoria.query.all()

    return render_template(
        "index.html",
        categorias=categorias,
        es_home=True,
    )

# ==========================
# Login administrador
# ==========================

@main.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        usuario = request.form["usuario"]
        password = request.form["password"]

        user = Usuario.query.filter_by(
            usuario=usuario
        ).first()

        if user and check_password_hash(
            user.password,
            password
        ):

            login_user(user)

            return redirect(
                url_for("main.admin")
            )

        return "Usuario o contraseña incorrectos"

    return render_template("login.html")


# ==========================
# Logout
# ==========================

@main.route("/logout")
def logout():

    logout_user()

    return redirect(
        url_for("main.login")
    )

# ==========================
# Panel de administración
# ==========================

@main.route("/admin")
@login_required
def admin():

    categorias = Categoria.query.all()
    productos = Producto.query.all()

    return render_template(
        "admin.html",
        categorias=categorias,
        productos=productos,
    )


# ==========================
# Agregar producto
# ==========================

@main.route("/admin/producto", methods=["POST"])
@login_required
def agregar_producto():

    nombre = request.form["nombre"]
    descripcion = request.form["descripcion"]
    categoria_id = request.form["categoria"]

    imagen = request.files.get("imagen")

    nombre_imagen = ""

    if imagen and imagen.filename:

        nombre_imagen = imagen.filename

        ruta = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            nombre_imagen,
        )

        imagen.save(ruta)

    producto = Producto(
        nombre=nombre,
        descripcion=descripcion,
        imagen=nombre_imagen,
        categoria_id=categoria_id,
    )

    db.session.add(producto)
    db.session.commit()

    return redirect(url_for("main.admin"))


# ==========================
# Editar producto
# ==========================

@main.route("/admin/producto/<int:id>/editar")
@login_required
def editar_producto(id):

    producto = Producto.query.get_or_404(id)
    categorias = Categoria.query.all()

    return render_template(
        "editar.html",
        producto=producto,
        categorias=categorias,
    )


# ==========================
# Guardar cambios
# ==========================

@main.route("/admin/producto/<int:id>/guardar", methods=["POST"])
@login_required
def guardar_producto(id):

    producto = Producto.query.get_or_404(id)

    producto.nombre = request.form["nombre"]
    producto.descripcion = request.form["descripcion"]
    producto.categoria_id = request.form["categoria"]

    imagen = request.files.get("imagen")

    if imagen and imagen.filename:

        nombre_imagen = imagen.filename

        ruta = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            nombre_imagen,
        )

        imagen.save(ruta)

        producto.imagen = nombre_imagen

    db.session.commit()

    return redirect(url_for("main.admin"))


# ==========================
# Eliminar producto
# ==========================

@main.route("/admin/producto/<int:id>/eliminar")
@login_required
def eliminar_producto(id):

    producto = Producto.query.get_or_404(id)

    if producto.imagen:

        ruta = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            producto.imagen,
        )

        if os.path.exists(ruta):
            os.remove(ruta)

    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for("main.admin"))

# ==========================
# Agregar categoría
# ==========================

@main.route("/admin/categoria", methods=["POST"])
def agregar_categoria():

    nombre = request.form["nombre"]

    imagen = request.files.get("imagen")

    nombre_imagen = ""

    if imagen and imagen.filename:

        nombre_imagen = imagen.filename

        ruta = os.path.join(
            current_app.root_path,
            "static",
            "images",
            "categorias",
            nombre_imagen
        )

        imagen.save(ruta)


    categoria = Categoria(
        nombre=nombre,
        imagen=nombre_imagen
    )

    db.session.add(categoria)
    db.session.commit()

    return redirect(url_for("main.admin"))

# ==========================
# Editar categoría
# ==========================

@main.route("/admin/categoria/<int:id>/editar")
@login_required
def editar_categoria(id):

    categoria = Categoria.query.get_or_404(id)

    return render_template(
        "editar_categoria.html",
        categoria=categoria,
    )


# ==========================
# Guardar cambios categoría
# ==========================

@main.route("/admin/categoria/<int:id>/guardar", methods=["POST"])
@login_required
def guardar_categoria(id):

    categoria = Categoria.query.get_or_404(id)

    categoria.nombre = request.form["nombre"]

    imagen = request.files.get("imagen")

    if imagen and imagen.filename:

        nombre_imagen = imagen.filename

        ruta = os.path.join(
            current_app.root_path,
            "static",
            "images",
            "categorias",
            nombre_imagen
        )

        imagen.save(ruta)

        categoria.imagen = nombre_imagen


    db.session.commit()

    return redirect(url_for("main.admin"))

# ==========================
# Eliminar categoría
# ==========================

@main.route("/admin/categoria/<int:id>/eliminar")
@login_required
def eliminar_categoria(id):

    categoria = Categoria.query.get_or_404(id)


    if categoria.productos:

        return "No se puede eliminar una categoría con productos asociados"


    if categoria.imagen:

        ruta = os.path.join(
            current_app.root_path,
            "static",
            "images",
            "categorias",
            categoria.imagen
        )


        if os.path.exists(ruta):
            os.remove(ruta)


    db.session.delete(categoria)
    db.session.commit()


    return redirect(url_for("main.admin"))

# ==========================
# Productos por categoría
# ==========================

@main.route("/categoria/<nombre>")
def categoria(nombre):

    categoria = Categoria.query.filter_by(
        nombre=nombre
    ).first_or_404()

    productos = Producto.query.filter_by(
        categoria_id=categoria.id
    ).all()

    return render_template(
        "categoria.html",
        categoria=categoria,
        productos=productos,
    )
# ==========================
# Cambiar contraseña
# ==========================

@main.route("/admin/cambiar-password", methods=["POST"])
@login_required
def cambiar_password():

    usuario = Usuario.query.get(current_user.id)

    password_actual = request.form["password_actual"]
    password_nueva = request.form["password_nueva"]
    password_confirmar = request.form["password_confirmar"]


    if not check_password_hash(
        usuario.password,
        password_actual
    ):
        return "La contraseña actual es incorrecta"


    if password_nueva != password_confirmar:
        return "Las contraseñas nuevas no coinciden"


    usuario.password = generate_password_hash(
        password_nueva
    )


    db.session.commit()


    return redirect(
        url_for("main.admin")
    )
