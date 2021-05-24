from flaskr import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return '<User: {}>'.format(self.username)