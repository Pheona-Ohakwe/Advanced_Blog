import os
from flask import Flask
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
from app.database import db, migrate
from app.swagger_docs import swaggerui_blueprint


load_dotenv()

cache = Cache()
limiter = Limiter(get_remote_address, default_limits=["100 per day"])

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///blog.db'

db.init_app(app)
migrate.init_app(app, db)

cache.init_app(app)
limiter.init_app(app)

app.register_blueprint(swaggerui_blueprint)

from app.routes import *

if __name__ == '__main__':
    app.run(debug=True)
