from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import User
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@db:5432/mydatabase'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 500
    app.config['SQLALCHEMY_MAX_OVERFLOW'] = 100
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 30  # Таймаут ожидания свободного соединения
    app.config['SQLALCHEMY_POOL_RECYCLE'] = 280  # Переподключение для предотвращения таймаутов

    db.init_app(app)

    with app.app_context(): 
        from app.routers.main_routes import main_bp
        from app.routers.auth_routes import auth_bp


        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)

        db.create_all()


        return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000)

