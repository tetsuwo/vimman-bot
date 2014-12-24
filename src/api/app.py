# -*- coding: utf-8 -*-
from flask import Flask

#API_ACCESS_KEY = 'himejimaspecial'
#LOG_FILENAME = 'example.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

app = Flask(__name__)
#app.secret_key = 'my secret key'

app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTING', silent=True)

# delete 
@app.before_request
def before_request():
    pass

# delete
@app.teardown_request
def teardown_request(exception):
    pass

from controllers.questions import questions 
app.register_blueprint(questions.app, url_prefix="/questions")

from controllers.operators import operators
app.register_blueprint(operators.app, url_prefix="/operators")

from controllers.informations import informations
app.register_blueprint(informations.app, url_prefix="/informations")

from controllers.responses import responses
app.register_blueprint(responses.app, url_prefix="/responses")

from controllers.tweets import tweets
app.register_blueprint(tweets.app, url_prefix="/tweets")

from controllers.users import users
app.register_blueprint(users.app, url_prefix="/users")

if __name__ == '__main__':
    app.run()
