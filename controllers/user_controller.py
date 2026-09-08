# controllers/user_controller.py
# Placeholder: controlador de ejemplo. Handlers async compatibles
# con la firma (request, response) del router de hardboiled.

async def list_users(req, res):
    # TODO: reemplazar con lógica real (consulta vía hardboiled/database.py)
    res.json({"users": []})


async def get_user(req, res):
    user_id = req.params.get("id")
    # TODO: reemplazar con consulta real
    res.json({"user_id": user_id})