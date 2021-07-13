from app.database.config.init_database import init_database
from flask import Flask

from app import register_routes

app = Flask(__name__)
app.config["DEBUG"] = True


@app.errorhandler(404)
def page_not_found(e):
    return {'message': 'Route not found'}, 404


register_routes(app)
init_database()

if __name__ == '__main__':
    app.run()
