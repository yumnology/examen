from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class Videojuego(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    desarrollador = db.Column(db.String(100), nullable=False)
    anio_lanzamiento = db.Column(db.Integer, nullable=False)
    plataforma = db.Column(db.String(100), nullable=False)
    clasificacion = db.Column(db.String(50), nullable=False)

    def __init__(self, titulo, desarrollador, anio_lanzamiento, plataforma, clasificacion):
        self.titulo = titulo
        self.desarrollador = desarrollador
        self.anio_lanzamiento = anio_lanzamiento
        self.plataforma = plataforma
        self.clasificacion = clasificacion

    def to_json(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'desarrollador': self.desarrollador,
            'anio_lanzamiento': self.anio_lanzamiento,
            'plataforma': self.plataforma,
            'clasificacion': self.clasificacion
        }
    
    def __repr__(self):
        return f'<Task {self.name}>'

@app.route('/videojuegos', methods=['POST'])
def add():
    if not request.json or not 'titulo' in request.json:
        abort(400)
    videojuego = Videojuego(
        titulo=request.json['titulo'],
        desarrollador=request.json.get('desarrollador', ""),
        anio_lanzamiento=request.json.get('anio_lanzamiento', 0),
        plataforma=request.json.get('plataforma', ""),
        clasificacion=request.json.get('clasificacion', "")
    )
    db.session.add(videojuego)
    db.session.commit()
    return jsonify(videojuego.to_json()), 201

@app.route('/videojuegos', methods=['GET'])
def get_all():
    videojuegos = Videojuego.query.all()
    return jsonify([videojuego.to_json() for videojuego in videojuegos])

@app.route('/videojuegos/<int:id>', methods=['GET'])
def get_one(id):
    videojuego = Videojuego.query.get_or_404(id)
    return jsonify(videojuego.to_json())

@app.route('/videojuegos/<int:id>', methods=['PUT'])
def update(id):
    videojuego = Videojuego.query.get_or_404(id)
    if not request.json:
        abort(400)

    videojuego.titulo = request.json.get('titulo', videojuego.titulo)
    videojuego.desarrollador = request.json.get('desarrollador', videojuego.desarrollador)
    videojuego.anio_lanzamiento = request.json.get('anio_lanzamiento', videojuego.anio_lanzamiento)
    videojuego.plataforma = request.json.get('plataforma', videojuego.plataforma)
    videojuego.clasificacion = request.json.get('clasificacion', videojuego.clasificacion)
    
    db.session.commit()
    return jsonify(videojuego.to_json())

@app.route('/videojuegos/<int:id>', methods=['DELETE'])
def delete(id):
    videojuego = Videojuego.query.get_or_404(id)
    db.session.delete(videojuego)
    db.session.commit()
    return jsonify({'result': True})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("Task added!")
    app.run(debug=True)
