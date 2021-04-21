from flask import Flask, jsonify
from controllers import front_controller

app = Flask(__name__)


front_controller.route(app)


if __name__ == '__main__':
    app.run(debug=True)
