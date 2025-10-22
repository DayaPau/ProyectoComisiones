from utils.database import db

class Regla(db.Model):
    __tablename__ = 'reglas'
    id = db.Column(db.Integer, primary_key=True)
    monto_minimo = db.Column(db.Float, nullable=False)
    porcentaje_comision = db.Column(db.Float, nullable=False)