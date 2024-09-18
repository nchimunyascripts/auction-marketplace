from flask import Flask, request
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'   
db = SQLAlchemy(app)

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, unique=True, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)

@app.route('/')
def hello_world():
    return "Hello World"

@app.route('/upload', methods=['POST'])
def update_world():
    pic = request.files["pic"]
    if not pic:
        return "No Picture"
    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    
    img = Img(img=pic.read(), mimetype=mimetype, name=filename)
    db.session.add(img)
    db.session.commit()
    return "Done!", 200
    
if __name__ == "__main__":
    app.run(debug=True)