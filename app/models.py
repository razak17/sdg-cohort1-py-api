from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()


def db_setup(app, database_path=None):
    db.app = app
    db.init_app(app)
    db.create_all()


class Log_entry(db.Model):
    __tablename__ = "api_logs"

    id = Column(Integer, primary_key=True)
    request_method = Column(String)
    path = Column(String)
    status_code = Column(Integer)
    response_time = Column(Integer)

    def __init__(self, request_method, path, status_code, response_time):
        self.request_method = request_method
        self.path = path
        self.status_code = status_code
        self.response_time = response_time

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def serialize(self):
        return f"{self.request_method}\t\t{self.path}\t\t{self.status_code}\t\t{str(self.response_time).zfill(2)}ms"
