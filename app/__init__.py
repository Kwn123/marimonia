from flask import Flask
from flask_login import LoginManager
from werkzeug.security import generate_password_hash

from .config import Config
from .models import db

login_manager = LoginManager()
login_manager.login_view = "main.login"

@login_manager.user_loader
def load_user(user_id):
    from .models import Usuario
    return Usuario.query.get(int(user_id))

def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():

        from .models import Categoria, Usuario

        db.create_all()

        if Usuario.query.filter_by(usuario="admin").first() is None:

            admin = Usuario(
                usuario="admin",
                password=generate_password_hash("admin123")
            )

            db.session.add(admin)
            db.session.commit()

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
                db.session.add(Categoria(nombre=nombre))

            db.session.commit()

    from .routes import main
    app.register_blueprint(main)

    return app
