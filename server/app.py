from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# function for earthquake response
def get_earthquake_response(data, status=200):
    return make_response(data, status)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return get_earthquake_response(body)

# earthquake by ID
@app.route('/earthquakes/<int:id>')
def earthquake_by_id(id):
    quake = Earthquake.query.filter_by(id=id).first()
    if quake:
        body = quake.to_dict()
        status = 200
    else:
        body = {'message': f'Earthquake {id} not found.'}
        status = 404
    return get_earthquake_response(body, status)

# earthquakes by magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquake_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    quake_data = [quake.to_dict() for quake in quakes]
    body = {'count': len(quakes), 'quakes': quake_data}
    return get_earthquake_response(body)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
