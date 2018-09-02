from flask import Flask
from views.account import ac
from views.codes import co

app = Flask(__name__)

app.config.from_object('settings.DevelopmentConfig')

app.register_blueprint(ac)
app.register_blueprint(co)


if __name__ == '__main__':
    app.run()



















