try:
    from flask import Flask
except ImportError:
    raise ImportError('flask packed was not found. Try `pip install .[api]`')
from flutter_app_routs import flutter_app
from web_routs import browser_app

def create_app():
    app = Flask(__name__)
    app.config['DATABASE_PATH'] = "/app/bills.db"
    app.register_blueprint(flutter_app)
    app.register_blueprint(browser_app)
    return app
    

# gunicorn happy now
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
