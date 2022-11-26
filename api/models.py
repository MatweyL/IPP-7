import datetime

from api import db, app


class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    brand = db.Column(db.String)
    price = db.Column(db.Integer)
    age = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "brand": self.brand,
            "price": self.price,
            "age": self.age
        }


with app.app_context():
    db.create_all()
    if not db.session.query(Car).get(1) or not db.session.query(Car).all():
        db.session.add(Car(title=f"Cool car {datetime.datetime.now()}", brand="Mercedes", price=5000000, age=3))
        db.session.commit()
