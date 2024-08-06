from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Создаем приложение Flask
app = Flask(__name__)

# Настройки подключения к базе данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создаем объект SQLAlchemy
db = SQLAlchemy(app)


# Определяем модель (таблицу в базе данных)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


# Создаем таблицу в базе данных
with app.app_context():
    db.create_all()


# Добавляем запись в базу данных
@app.route('/add_user')
def add_user():
    new_user = User(username='JohnDoe')
    db.session.add(new_user)
    db.session.commit()
    return 'Пользователь добавлен в базу данных'


# Получаем все записи из базы данных
@app.route('/users')
def get_users():
    users = User.query.all()
    return str(users)


# Запускаем приложение
if __name__ == '__main__':
    app.run()
