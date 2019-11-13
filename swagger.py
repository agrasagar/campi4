from flask_swagger_ui import get_swaggerui_blueprint

def initialize_swagger(app):
    swagger_url = '/swagger'
    api_url = '/static/swagger.json'
    blueprint = get_swaggerui_blueprint(
        swagger_url,
        api_url,
        config={
            'app_name': "campi4"
        }
    )
    app.register_blueprint(blueprint, url_prefix=swagger_url)