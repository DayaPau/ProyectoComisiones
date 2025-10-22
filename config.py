import os

class Config:
    SECRET_KEY = 'tu-clave-secreta-aqui'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/minicore.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False