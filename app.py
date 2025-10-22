from flask import Flask
from utils.database import db
from flask_migrate import Migrate
import os

# ===== Config =====
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Si hay DATABASE_URL (Render) úsalo; si no, usa SQLite local
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'db.sqlite3')}"
else:
    # 🔹 Corrige prefijo para compatibilidad con psycopg3
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', 'dev')

# ===== Inicialización de BD =====
db.init_app(app)
migrate = Migrate(app, db)

print("🗄️ DATABASE_URL ->", app.config['SQLALCHEMY_DATABASE_URI'])

# ===== Importar Modelos =====
from models.vendedor import Vendedor
from models.venta import Venta
from models.regla import Regla

def seed_data():
    """Si no hay vendedores, sembramos datos iniciales (portable para SQLite/Postgres)."""
    if db.session.query(Vendedor).first():
        print("ℹ️ La base ya tiene datos; no se sembró de nuevo.")
        return

    # Reglas (ojo: porcentajes como decimales)
    reglas = [
        Regla(id=1, monto_minimo=1000, porcentaje_comision=0.15),
        Regla(id=2, monto_minimo=800, porcentaje_comision=0.10),
        Regla(id=3, monto_minimo=600, porcentaje_comision=0.06),
        Regla(id=4, monto_minimo=500, porcentaje_comision=0.08),
    ]

    vendedores = [
        Vendedor(id=1, nombre='Perico P'),
        Vendedor(id=2, nombre='Zoila B'),
        Vendedor(id=3, nombre='Aquiles C'),
        Vendedor(id=4, nombre='Johny M'),
    ]

    ventas = [
        Venta(id=1,  fecha_venta='2025-05-21', vendedor_id=1, cuota_monto=400.00),
        Venta(id=2,  fecha_venta='2025-05-29', vendedor_id=2, cuota_monto=600.00),
        Venta(id=3,  fecha_venta='2025-06-03', vendedor_id=2, cuota_monto=200.00),
        Venta(id=4,  fecha_venta='2025-06-09', vendedor_id=1, cuota_monto=300.00),
        Venta(id=5,  fecha_venta='2025-06-11', vendedor_id=3, cuota_monto=900.00),
        Venta(id=6,  fecha_venta='2025-06-15', vendedor_id=4, cuota_monto=1000.00),
        Venta(id=7,  fecha_venta='2025-06-20', vendedor_id=1, cuota_monto=1200.00),
        Venta(id=8,  fecha_venta='2025-06-25', vendedor_id=2, cuota_monto=800.00),
        Venta(id=9,  fecha_venta='2025-07-01', vendedor_id=3, cuota_monto=500.00),
        Venta(id=10, fecha_venta='2025-07-05', vendedor_id=4, cuota_monto=700.00),
    ]

    db.session.add_all(reglas + vendedores + ventas)
    db.session.commit()
    print("✅ Datos iniciales sembrados.")

# ===== Crear tablas y sembrar datos =====
with app.app_context():
    db.create_all()
    seed_data()

# ===== Registrar Blueprint =====
from controllers.venta_controller import main_blueprint
app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=True)
