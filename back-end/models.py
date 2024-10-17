from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    complete_name = db.Column(db.String, nullable=False, name='nombre')
    password = db.Column(db.String, nullable=False, name='contraseña')
    email = db.Column(db.String, unique=True, nullable=False, name='correo')
    date_registered = db.Column(db.String, nullable=False, name='fecha_creacion')

    destinations = db.relationship('Destination', backref='user', lazy=True, cascade="all, delete-orphan")
    histories = db.relationship('History', backref='user', lazy=True, cascade="all, delete-orphan")


class Destination(db.Model):
    __tablename__ = 'rutas'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, name='id_usuario')
    departure = db.Column(db.String, nullable=False, name='ubicacion_inicial')
    destination = db.Column(db.String, nullable=False, name='ubicacion_final')
    duration = db.Column(db.Integer, nullable=False, name='duracion_estimada_minutos')
    date_registered = db.Column(db.DateTime, nullable=False, name='fecha_creacion')  # Changed to DateTime
    transportation = db.Column(db.String, nullable=False, name='medio_esperado')

    histories = db.relationship('History', backref='destination', lazy=True)

class History(db.Model):
    __tablename__ = 'historial_rutas'
    
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('rutas.id'), nullable=False, name='id_ruta')  # Aligning with 'id_ruta'
    user_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, name='id_usuario')  # Aligning with 'id_usuario'
    start_time = db.Column(db.String, nullable=False, name='hora_inicio')  # Aligning with 'hora_inicio'
    finish_time = db.Column(db.String, nullable=False, name='hora_fin')  # Aligning with 'hora_fin'
    distance = db.Column(db.Float, nullable=False, name='distanciakm')  # Aligning with 'distanciakm'
    path = db.Column(db.Text, nullable=False, name='camino')  # Aligning with 'camino'
    transportation = db.Column(db.String, nullable=False, name='medio_usado')  # Aligning with 'medio_usado'
