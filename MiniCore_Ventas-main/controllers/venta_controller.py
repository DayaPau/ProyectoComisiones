from flask import Blueprint, render_template, request
from models.vendedor import Vendedor
from models.venta import Venta
from models.regla import Regla
from datetime import datetime

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/', methods=['GET', 'POST'])
def resumen_comisiones():
    comisiones = []
    fecha_inicio = request.form.get('fecha_inicio')
    fecha_fin = request.form.get('fecha_fin')

    vendedores = Vendedor.query.all()
    reglas = Regla.query.order_by(Regla.monto_minimo.desc()).all()

    for vendedor in vendedores:
        if fecha_inicio and fecha_fin:
            fi = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            ff = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            ventas = Venta.query.filter(
                Venta.vendedor_id == vendedor.id,
                Venta.fecha_venta >= fi,
                Venta.fecha_venta <= ff
            ).all()
        else:
            ventas = Venta.query.filter_by(vendedor_id=vendedor.id).all()
        total = sum(v.cuota_monto for v in ventas)
        porcentaje = 0
        for regla in reglas:
            if total >= regla.monto_minimo:
                porcentaje = regla.porcentaje_comision
                break
        comision = total * porcentaje
        comisiones.append({
            'vendedor': vendedor.nombre,
            'total_ventas': total,
            'porcentaje': porcentaje,
            'comision': comision
        })
    return render_template('index.html', comisiones=comisiones, fecha_inicio=fecha_inicio, fecha_fin=fecha_fin)