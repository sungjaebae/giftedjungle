from flask import Flask
from routes.authentication import authentication
from routes.gift import gift, gift_list
from routes.notification import notification
app = Flask(__name__)


@app.route('/')
def index():
    return gift_list()


app.register_blueprint(authentication)
app.register_blueprint(gift)
app.register_blueprint(notification)
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
