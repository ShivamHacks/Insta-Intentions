from flask import Flask, jsonify, request
import inspect
from database import Database

app = Flask(__name__)
database = Database()


def add_routes_for_object(obj, app):
    for method_name in dir(obj):
        method = getattr(obj, method_name)

        if callable(method) and not method_name.startswith("__"):
            signature = inspect.signature(method)
            param_names = list(signature.parameters.keys())

            def create_route(method_name, param_names):
                def route():
                    args = {}
                    for key in param_names:
                        value = request.args.get(key)
                        if value is None:
                            return jsonify(error=f"Parameter {key} is required")
                        args[key] = value
                    method_to_call = getattr(obj, method_name)
                    result = method_to_call(**args)
                    return jsonify(result=result)

                return route

            app.add_url_rule(
                f"/{method_name}",
                method_name,
                create_route(method_name, param_names),
                methods=["GET"],
            )


add_routes_for_object(database, app)

if __name__ == "__main__":
    app.run(debug=True)
