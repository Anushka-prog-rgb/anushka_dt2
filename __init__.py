from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # MySQL config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passw0rd@localhost:3308/app_db?charset=utf8mb4'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Register blueprints
    from .weather import weather_bp
    from .student_info import student_bp
    from .app_with_mysql_db import user_bp, task_bp

    app.register_blueprint(weather_bp, url_prefix="/api/weather")
    app.register_blueprint(student_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(task_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()

    return app



