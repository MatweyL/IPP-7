import pprint

from api import app


from ariadne import load_schema_from_path, make_executable_schema, \
    graphql_sync, snake_case_fallback_resolvers, ObjectType
from ariadne.constants import PLAYGROUND_HTML
from flask import request, jsonify

from api.mutations import create_car_resolver, update_car_resolver, delete_car_resolver
from api.queries import listCars_resolver, getCar_resolver

query = ObjectType("Query")
mutation = ObjectType("Mutation")
query.set_field("listCars", listCars_resolver)
query.set_field("getCar", getCar_resolver)
mutation.set_field("createCar", create_car_resolver)
mutation.set_field("updateCar", update_car_resolver)
mutation.set_field("deleteCar", delete_car_resolver)

type_defs = load_schema_from_path("schema.graphql")
schema = make_executable_schema(
    type_defs, query, mutation, snake_case_fallback_resolvers
)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    pprint.pprint(request.get_json())
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run()
