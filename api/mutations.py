from ariadne import convert_kwargs_to_snake_case

from api import db
from api.models import Car


@convert_kwargs_to_snake_case
def create_car_resolver(obj, info, title, brand, price, age):
    try:
        car = Car(title=title, brand=brand, price=price, age=age)
        db.session.add(car)
        db.session.commit()
        payload = {
            "success": True,
            "car": car.to_dict()
        }
    except BaseException as e:
        payload = {
            "success": False,
            "errors": [str(e)]
        }
    return payload


def set_if_updated(obj, field, value):
    if field:
        obj.__setattr__(field, value)


@convert_kwargs_to_snake_case
def update_car_resolver(obj, info, id, title, brand, price, age):
    try:
        car = Car.query.get(id)
        if car:
            set_if_updated(car, "title", title)
            set_if_updated(car, "brand", brand)
            set_if_updated(car, "price", price)
            set_if_updated(car, "age", age)
        db.session.add(car)
        db.session.commit()
        payload = {
            "success": True,
            "post": car.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"item matching id {id} not found"]
        }
    return payload


@convert_kwargs_to_snake_case
def delete_car_resolver(obj, info, id):
    try:
        car = Car.query.get(id)
        db.session.delete(car)
        db.session.commit()
        payload = {"success": True, "car": car.to_dict()}
    except BaseException as e:
        payload = {
            "success": False,
            "errors": [f"Not found with id {id}"]
        }
    return payload
