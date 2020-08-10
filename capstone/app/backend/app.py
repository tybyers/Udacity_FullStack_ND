from api import create_app
from flask_migrate import Migrate
from models import db

app = create_app()
migrate = Migrate(app, db)


## ------------------------
## Launch app
## ------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)