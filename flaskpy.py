from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@192.168.18.208:3306/uimsp_db'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True)
    image = db.Column(db.String(200))
    registerDate = db.Column(db.DateTime, default=datetime.utcnow)
    biography = db.Column(db.String(500))
    user_type_id = db.Column(db.Integer)

# Crear todas las tablas
with app.app_context():
    db.create_all()

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data['name'],
        username=data['username'],
        password=data['password'],
        phone=data['phone'],
        email=data['email'],
        image=data['image'],
        registerDate=datetime.strptime(data['registerDate'], '%Y-%m-%d %H:%M:%S'),
        biography=data['biography'],
        user_type_id=data['user_type_id']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created'})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'})
    
    user.name = data['name']
    user.username = data['username']
    user.password = data['password']
    user.phone = data['phone']
    user.email = data['email']
    user.image = data['image']
    user.registerDate = datetime.strptime(data['registerDate'], '%Y-%m-%d %H:%M:%S')
    user.biography = data['biography']
    user.user_type_id = data['user_type_id']
    
    db.session.commit()
    return jsonify({'message': 'User updated'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'})
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'password': user.password,
        'phone': user.phone,
        'email': user.email,
        'image': user.image,
        'registerDate': user.registerDate.strftime('%Y-%m-%d %H:%M:%S'),
        'biography': user.biography,
        'user_type_id': user.user_type_id
    } for user in users])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
