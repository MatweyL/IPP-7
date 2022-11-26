from ariadne import convert_kwargs_to_snake_case

from .models import Car


def listCars_resolver(obj, info):
    try:
        cars = [car.to_dict() for car in Car.query.all()]
        print(cars)
        payload = {
            "success": True,
            "cars": cars
        }
    except Exception as error:
        payload = {
            "success": False,
            "errors": [str(error)]
        }
    return payload


@convert_kwargs_to_snake_case
def getCar_resolver(obj, info, id):
    try:
        car = Car.query.get(id)
        payload = {
            "success": True,
            "car": car.to_dict()
        }
    except AttributeError:
        payload = {
            "success": False,
            "errors": [f"Post item matching {id} not found"]
        }
    return payload
