from lw.app import db, app
from lw.app.models import User


with app.app_context():
    db.create_all()

