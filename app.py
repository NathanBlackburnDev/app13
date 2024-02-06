from flask import Flask
from datetime import timedelta

# Set app variables
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ajfoiwuo21rwaf'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

import routes

# Run Flask app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
