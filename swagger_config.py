template = {
    "swagger": "2.0",
    "info": {
        "title": "API MAFEFIBER",
        "description": "API para gestionar servicios de MAFEFIBER",
        "version": "1.0.0",
        "contact": {
            "name": "Soporte MAFEFIBER",
            "email": "soporte@mafefiber.com"
        }
    }
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "title": "API MAFEFIBER",
    "version": "1.0.0",
    "description": "API para gestionar servicios de MAFEFIBER"
}