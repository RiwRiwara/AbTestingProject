from flask import Blueprint

defaultAPI = Blueprint('defaultAPI', __name__)
authAPI = Blueprint('authAPI', __name__)
apiAPI = Blueprint('apiAPI', __name__)

from . import wep
from . import auth
from . import api
