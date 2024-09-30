from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import and_


app = Flask(__name__)
CORS(app)

cloud_sql_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME', 'mtc-cloud101:us-central1:cars')

# Configure SQLAlchemy to use Unix socket
socket_dir = '/cloudsql'
socket_path = f'{socket_dir}/{cloud_sql_connection_name}'

is_local = os.environ.get('LOCAL_DEV') == '1'
db_user = os.environ.get('DB_USER', 'postgres')
db_pass = os.environ.get('DB_PASS', 'password')
db_name = os.environ.get('DB_NAME', 'postgres')
db_host = os.environ.get('DB_HOST', 'localhost')

# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}?host={socket_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

if is_local:
    # Local SQLite database
    print("Running in local environment")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_pass}@{db_host}/{db_name}'
else:
    # Cloud SQL connection details
    db_user = os.environ.get('DB_USER', "postgres")
    db_pass = os.environ.get('DB_PASS', 'password')
    db_name = os.environ.get('DB_NAME', 'postgres')

    # Configure SQLAlchemy to use Unix socket in production
    socket_dir = '/cloudsql'
    socket_path = f'{socket_dir}/{cloud_sql_connection_name}'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{db_user}:{db_pass}@/{db_name}?host={socket_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Car model
class Car(db.Model):
    __tablename__ = 'cars'
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255))
    mileage = db.Column(db.Integer)
    fuel_type = db.Column(db.String(20))

    def to_dict(self):
        return {
            'id': self.id,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'price': self.price,
            'image': self.image,
            'mileage': self.mileage,
            'fuel_type': self.fuel_type
        }

# Routes
@app.route('/api/cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    print(cars[0].to_dict())
    return jsonify([car.to_dict() for car in cars])

@app.route('/api/cars/<int:car_id>', methods=['GET'])
def get_car(car_id):
    car = Car.query.get_or_404(car_id)
    return jsonify(car.to_dict())

@app.route('/api/cars', methods=['POST'])
def create_car():
    data = request.json
    new_car = Car(
        make=data['make'],
        model=data['model'],
        year=data['year'],
        price=data['price'],
        image=data.get('image'),
        mileage=data.get('mileage'),
        fuel_type=data.get('fuel_type')
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify(new_car.to_dict()), 201

@app.route('/api/cars/<int:car_id>', methods=['PUT'])
def update_car(car_id):
    car = Car.query.get_or_404(car_id)
    data = request.json
    car.make = data.get('make', car.make)
    car.model = data.get('model', car.model)
    car.year = data.get('year', car.year)
    car.price = data.get('price', car.price)
    car.image = data.get('image', car.image)
    car.mileage = data.get('mileage', car.mileage)
    car.fuel_type = data.get('fuel_type', car.fuel_type)
    db.session.commit()
    return jsonify(car.to_dict())

@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    db.session.delete(car)
    db.session.commit()
    return '', 204

@app.route('/api/cars/search', methods=['GET'])
def search_cars():
    make = request.args.get('make')
    model = request.args.get('model')
    min_year = request.args.get('min_year', type=int)
    max_year = request.args.get('max_year', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_mileage = request.args.get('min_mileage', type=int)
    max_mileage = request.args.get('max_mileage', type=int)
    fuel_type = request.args.get('fuel_type')

    print(request.args)

    query = Car.query

    filters = []
    if make:
        filters.append(Car.make.ilike(f'%{make}%'))
    if model:
        filters.append(Car.model.ilike(f'%{model}%'))
    if min_year:
        filters.append(Car.year >= min_year)
    if max_year:
        filters.append(Car.year <= max_year)
    if min_price:
        filters.append(Car.price >= min_price)
    if max_price:
        filters.append(Car.price <= max_price)
    if min_mileage:
        filters.append(Car.mileage >= min_mileage)
    if max_mileage:
        filters.append(Car.mileage <= max_mileage)
    if fuel_type:
        filters.append(Car.fuel_type.ilike(f'%{fuel_type}%'))

    if filters:
        query = query.filter(and_(*filters))

    cars = query.all()
    return jsonify([car.to_dict() for car in cars])

if __name__ == '__main__':
    if is_local:
        app.run(debug=True, host='localhost', port=5000)
    else:
        app.run(host='0.0.0.0', port=8080)