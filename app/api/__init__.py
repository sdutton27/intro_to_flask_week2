from flask import Blueprint


# we need to specify url prefix
# like in PokeAPI everything will be pokeapi.co/api/v2/<EVERYTHING ELSE GOES HERE>
# we don't want these prefixes every time

api = Blueprint('api', __name__, url_prefix='/api') # we don't need to specify template folder

# eventually they will all be connected to this api
from . import auth_routes, ig_routes, shop_routes
