# routes/user_routes.py
# Placeholder: define las rutas del recurso "user" y las conecta con su controlador.

from controllers.user_controller import list_users, get_user


def register_user_routes(app):
    app.get("/users")(list_users)
    app.get("/users/:id")(get_user)