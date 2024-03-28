from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)

# Create the database tables based on the model
with app.app_context():
    db.create_all()
    print("Database and tables created successfully.")

@app.route('/submit', methods=['POST'])
def submit():
    if not request.form or 'name' not in request.form or 'email' not in request.form:
        print("Bad request: Missing name or email.")
        return jsonify({'error': 'Bad request'}), 400

    name = request.form['name']
    email = request.form['email']
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()

    print(f"Added user: {name}, Email: {email}")
    return jsonify({'success': True, 'message': 'User added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)
