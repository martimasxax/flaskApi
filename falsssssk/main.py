from flask import Flask
from src.api.routes import init_api_routes
from src.config.db import engine, test_connection
from src.config.base import Base

app = Flask(__name__)

init_api_routes(app)

test_connection()

if __name__ == '__main__':

    Base.metadata.create_all(bind=engine)
    app.run(debug=True)
