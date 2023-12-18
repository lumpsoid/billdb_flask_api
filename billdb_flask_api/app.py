try:
    from flask import Flask
except ImportError:
    raise ImportError('flask packed was not found. Try `pip install .[api]`')
from billdb_flask_api.flutter_app_routs import flutter_app
from billdb_flask_api.web_routs import browser_app

import logging

app = Flask(__name__)

# Configure Flask logging
# app.logger.setLevel(logging.DEBUG)  # Set the desired logging level
# # handler = logging.FileHandler("./flask.log")  # Replace with the desired path inside the container
# handler = logging.StreamHandler()
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )

# handler.setLevel(level=logging.DEBUG)  # Set the desired logging level for Flask logs
# app.logger.addHandler(handler)

app.register_blueprint(flutter_app)
app.register_blueprint(browser_app)

if __name__ == '__main__':
    app.run(debug=True)
