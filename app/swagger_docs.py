from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs' 
API_URL = '/static/swagger.yaml' 

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config = {
        'app_name': 'Coding Temple E-Commerce'
    }
)