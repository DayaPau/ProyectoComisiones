from utils.database import db

class Vendedor(db.Model):
    __tablename__ = 'vendedores'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    ventas = db.relationship('Venta', backref='vendedor', lazy=True)