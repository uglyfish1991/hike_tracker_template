from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hikes.db'
db = SQLAlchemy(app)

class Hike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_hike', methods=['POST'])
def add_hike():
    data = request.json
    new_hike = Hike(latitude=data['latitude'], longitude=data['longitude'], description=data['description'])
    db.session.add(new_hike)
    db.session.commit()
    return jsonify({'message': 'Hike added successfully'})

@app.route('/get_hikes', methods=['GET'])
def get_hikes():
    hikes = Hike.query.all()
    hikes_list = [{'latitude': hike.latitude, 'longitude': hike.longitude, 'description': hike.description} for hike in hikes]
    return jsonify(hikes_list)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)