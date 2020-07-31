from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import mooves_app
from models import db

migrate = Migrate(mooves_app, db)
manager = Manager(mooves_app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
