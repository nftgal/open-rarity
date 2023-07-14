import logging
import os

from flask import Flask

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


if __name__ == "__main__":
    app = Flask(__name__)

    if os.environ.get("FLASK_ENV", "development") == "production":
        app.debug = False
    else:
        app.debug = True

    from routes import main_routes
    app.register_blueprint(main_routes)
    
    app.run(host='0.0.0.0')
