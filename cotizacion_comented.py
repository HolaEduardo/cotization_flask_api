import requests
# Importamos la libreria datetime para obtener la fecha y hora actual
from datetime import datetime

#  ----------- Descomentar para testeo ------------
# Pedimos por consola el tiempo estimado y descuento para Bsale
#tiempo_estimado_bsale = float(input("Ingrese el tiempo estimado en horas para el desarrollo del plugin de Mercado Libre: "))
#discount_bsale = float(input("Ingrese el descuento para Bsale: "))
## Pedimos por consola el tiempo estimado y descuento para desde cero
#tiempo_estimado_scratch = float(input("Ingrese el tiempo estimado en horas para el desarrollo del e-commerce desde cero: "))
#discount_scratch = float(input("Ingrese el descuento para el desarrollo desde cero: "))
# ---------------------- Fin comentado ----------------------------

# ------------ Comentar para testeo ----------------------------------------------------------------------------------------------
# Importamos flask para crear la aplicacion web
from flask import Flask, render_template, request, redirect, jsonify, url_for
# Importamos cors para habilitar el acceso a la API desde cualquier origen o alguno en especifico
from flask_cors import CORS

# Creamos una instancia de Flask
app = Flask(__name__)

# Habilitamos el acceso a la API desde cualquier origen
CORS(app, resources={r"/*": {"origins": "*"}})

# Creamos la ruta para la API con metodo POST y endpoint /cotizacion
@app.route('/cotizacion', methods=['POST'])
#Definimos la funcion cotizacion que llamará al resto de funciones para obtener los datos y devolverá un JSON con los datos
def cotizacion():
    # Obtenemos los datos enviados desde el front-end en formato JSON
    data = request.get_json()
    # Obtenemos los datos de tiempo estimado y descuento para Bsale
    tiempo_estimado_bsale = int(data['tiempo_estimado_bsale'])
    # Obtenemos los datos de tiempo estimado y descuento para Bsale
    discount_bsale = int(data['discount_bsale'])
    # Obtenemos los datos de tiempo estimado y descuento para Bsale
    tiempo_estimado_scratch = int(data['tiempo_estimado_scratch'])
    # Obtenemos los datos de tiempo estimado y descuento para Bsale
    discount_scratch = int(data['discount_scratch'])
    # Obtenemos el valor del colaborador para Bsale
    colaborador_bsale = cotizationbsale.valueColabBsale(tiempo_estimado_bsale, discount_bsale)
    # Obtenemos el costo bruto mensual y anual para Bsale
    costo_bsale = cotizationbsale.costsMonthBsale()
    # Obtenemos el costo de activacion para Bsale
    costo_activacion_bsale = cotizationbsale.costActivateBsale()
    # Obtenemos el valor del colaborador para Scratch
    colaborador_scratch = cotizationfromscratch.valueColabfromScratch(tiempo_estimado_scratch, discount_scratch)
    # Obtenemos el costo bruto mensual y anual para Scratch
    costo_scratch = cotizationfromscratch.costsFromScratch()


    # Creamos un diccionario para guardar los datos de la cotizacion, recolectando los datos de las funciones anteriores
    cotizacion_data = {
        # Enviamos los valores de la UF, Dolar y la fecha de actualizacion
        "values": {
            "values_date": get_value()[1],
            "value_dolar": get_value()[2],
            "value_UF": get_value()[0],
        },
        # Enviamos la cotizacion para Bsale
        "cotization_one": {
            "cotization_date": dataTime(),
            "costo_bruto_bsale_mensual": round(costo_bsale),
            "costo_bruto_anual_bsale": round(costo_bsale * 12),
            "costo_IVA_mensual": round(costo_bsale * 0.19),
            "costo_IVA_anual": round(costo_bsale * 0.19) * 12,
            "costo_IVA_incl_bsale_mensual": round(costo_bsale * 1.19),
            "costo_IVA_incl_bsale_anual": round(costo_bsale * 1.19),
            "costo_activacion_bsale_bruto": round(costo_activacion_bsale),
            "costo_activacion_bsale_IVA": round(costo_activacion_bsale * 0.19),
            "costo_activacion_bsale_IVA_incl": round(costo_activacion_bsale * 1.19),
            "total_dev": round(colaborador_bsale),
            "total_costo_bruto": round(costo_activacion_bsale + colaborador_bsale),
            "total_iva_activacion": round(costo_activacion_bsale * 0.19),
            "total_costo_activacion_bsale": round((costo_activacion_bsale * 1.19) + colaborador_bsale),
        },
        # Enviamos la cotizacion para Scratch
        "cotization_two": {
            "cotization_date": dataTime(),
            "Valor_de_colaboradores": round(colaborador_scratch),
            "server_low_traffic_month": round(costo_scratch[0]),
            "server_low_traffic_year": round(costo_scratch[0]) * 12,
            "server_high_traffic_month ": round(costo_scratch[1]),
            "server_high_traffic_year": round(costo_scratch[1] * 12),
            "total_value_scratch": round(costo_scratch[1]) + colaborador_scratch
        }
    }
    # Retornamos el diccionario en formato JSON
    return jsonify(cotizacion_data)
# ------------------------------------ Fin comentado ------------------------------------------------------------------------------------------------------------------------------


# Definimos la funcion dataTime que nos devolverá la fecha y hora actual
def dataTime():
    # Obtenemos la fecha y hora actual
    now = datetime.now()
    # Definimos el formato de la fecha y hora
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    # Retornamos la fecha y hora actual en formato string
    return current_time

# Definimos la funcion get_value que nos devolverá el valor de la UF y el valor del dolar
def get_value():
    # Obtenemos los datos de la API de indicadores economicos
    r = requests.get('https://mindicador.cl/api')
    # Convertimos los datos en formato JSON
    valor = r.json()
    # Obtenemos el valor del dolar y lo redondeamos
    dollar = valor["dolar"]["valor"]
    # Obtenemos el valor de la UF y lo redondeamos
    uf = valor["uf"]["valor"]
    # Obtenemos la fecha de la UF
    fecha_str = valor["uf"]["fecha"]
    # Convertimos la fecha en formato datetime
    fecha_dt = datetime.fromisoformat(fecha_str.replace("Z", ""))
    # Redondeamos los valores del dolar
    dollar_entero = round(dollar)
    # Redondeamos los valores de la UF
    uf_entero = round(uf)
    # Retornamos los valores de la UF y el dolar y la fecha de observacion
    return uf_entero, fecha_dt, dollar_entero

# Definimos la clase para bsale
class cotizationbsale:
    # Definimos la funcion para obtener el valor de los costos fijos mensuales
    def costsMonthBsale():
        # Obtenemos el valor de la UF y lo multiplicamos por el valor de las integraciones de Bsale mensuales
        mercadoLibre = 0.7 * get_value()[0]
        webPay = 0.95 * get_value()[0]
        ecommerce = get_value()[0]
        # Sumamos los valores de las integraciones
        totalMonth = mercadoLibre + webPay + ecommerce
        # Retornamos el valor de los costos fijos mensuales de bsale
        return round(totalMonth)
    
    def costActivateBsale():
        # Obtenemos el valor de la UF y lo multiplicamos por el valor de la activación de Bsale
        uf = get_value()[0]
        mercadoLibre = 0.7 * uf
        ecommerce = uf
        activateBsale = mercadoLibre + ecommerce
        # Retornamos el valor de la activación de bsale
        return round(activateBsale)
    
    # Definimos la funcion para obtener el valor de los costos fijos anuales
    def valueColabBsale(tiempo_estimado_bsale, discount_bsale):
        # Obtenemos el valor del descuento aplicado y lo convertimos en porcentaje (100 con 50%) 60 / 100 = 0.6 -> 1 - 0.6 = 0.4
        discount = discount_bsale / 100
        discount = 1 - discount
        # Obtenemos el valor de la UF y lo multiplicamos por el descuento de colaborador
        valorHora = get_value()[0] * discount
        # Multiplicamos el valor hora con el descuento aplicado por el tiempo estimado de desarrollo
        totalColab = valorHora * tiempo_estimado_bsale
        # Retornamos el valor de los costos fijos anuales de bsale
        return round(totalColab)

# ---------- Descomentar para testeos -----------------------------------------------------------------------------------------------------------------------------
#    def printCoti():    
#        colaborador = cotizationbsale.valueColabBsale(tiempo_estimado_bsale, discount_bsale)
#        costoBsale = cotizationbsale.costsMonthBsale()
#        print("Cotización de servicio con e-commerce Eduardo Chateau")
#        print("Cotizcaión de servicio con e-commerce Bsale")
#        print("Fecha y hora de la cotización: " + str(dataTime()))
#        print("Fecha y hora del valor de la UF y el dolar observado: " + str(get_value()[1]))
#        print("Valor del dolar observado: $" + str(get_value()[2]))
#        print("Valor de la UF observado: $" + str(get_value()[0]))
#        print("Valor de un desarrollador: $" + str(round(colaborador)))
#        print("Costo bruto bsale mensual: $" + str(costoBsale))
#        print("Costo bruto anual bsale: $" + str(round(costoBsale * 12)))
#        print("Costo IVA mensual: $" + str(round(costoBsale * 0.19)))
#        print("Costo IVA anual: $" + str((round(costoBsale * 0.19) * 12)))
#        print("Costo con IVA incluido bsale mensual: $" + str(round(costoBsale * 1.19)))
#        print("Costo con IVA incluido bsale anual: $" + str(round((costoBsale * 1.19) * 12)))
#        print("Costo de activación de bsale: $" + str(cotizationbsale.costActivateBsale()))
#        print("Costo primer mes, activación más primer mes de servicio más IVA: $" + str(cotizationbsale.costActivateBsale() + round(costoBsale * 1.19)))
#        print("Valor total con IVA incluido de servicio bsale con desarrollo e intetgración de Plugin Mercado Libre,  mas 1 año de : $" + str(round(costoBsale + colaborador)))
#
# ---------- Fin de comentario-----------------------------------------------------------------------------------------------------------------------------

# Definimos la clase para cotización desde cero
class cotizationfromscratch():
    # Definimos la funcion para obtener el valor de los costos fijos mensuales
    def costsFromScratch():
        # Obtenemos el valor del dolar y lo multiplicamos por el valor del servidor mensual para sacar el CLP
        # Servidor bajo tráfico $14
        servidorBajo = get_value()[2] * 14
        # Servidor alto tráfico $100
        servidorAlto = get_value()[2] * 100
        # Retornamos el valor de los costos fijos mensuales para servidor bajo y alto tráfico respectivamente
        return servidorBajo, servidorAlto
    
    # Definimos la función para obtener el valor de la hora de un colaborador para el desarrollo de un e-commerce desde cero
    def valueColabfromScratch(tiempo_estimado, discount):
        # Obtenemos el valor del descuento aplicado y lo convertimos en porcentaje ($100 con 60%) 60 / 100 = 0.6 -> 1 - 0.6 = 0.4 - > 100 * 0.4 = $40, valor final $40 dolares de $100 con 60% de descuento    
        discount = discount / 100
        discount = 1 - discount
        # Obtenemos el valor de la UF y lo multiplicamos por el descuento de colaborador
        valorHora = get_value()[0] * discount
        # Multiplicamos el valor hora con el descuento aplicado por el tiempo estimado de desarrollo
        totalColab = valorHora * tiempo_estimado
        # Retornamos el valor del colaborador
        return round(totalColab)
    
# ---------- Descomentar para testeos -----------------------------------------------------------------------------------------------------------------------------
#S    def printCoti():
#S        colaborador = cotizationfromscratch.valueColabfromScratch(tiempo_estimado_scratch, discount_scratch)
#S        costoFromScratch = cotizationfromscratch.costsFromScratch()
#S        print("Cotización de servicio con e-commerce desde cero")
#S        print("Fecha y hora de la cotización: " + str(dataTime()))
#S        print("Fecha y hora del valor de la UF y el dolar observado: " + str(get_value()[1]))
#S        print("Valor del dolar observado: $" + str(get_value()[2]))
#S        print("Valor de la UF observado: $" + str(get_value()[0]))
#S        print("Valor de colaboradores: $" + str(round(colaborador)))
#S        print("Costo mensual servidor de bajo tráfico: $" + str(round(costoFromScratch[0])))
#S        print("Costo anual servidor de bajo tráfico: $" + str(round(costoFromScratch[0]) * 12))
#S        print("Costo mensual servidor de alto tráfico: $" + str(round(costoFromScratch[1])))
#S        print("Costo anual servidor de alto tráfico: $" + str(round(costoFromScratch[1] * 12)))
#S        
#S        print("Valor total incluido de servicio desde cero con desarrollo e intetgración de apis Mercado Libre, Bsale y WebPay mas costos por un año : $" + str(round(costoFromScratch[1]) + colaborador))
#S
#cotizationbsale.printCoti()
#print("-----------------------------------------------")
#cotizationfromscratch.printCoti()

#--------- Fin de comentado -----------------------------------------------------------------------------------------------------------------------------

# ----------------- Comentar para testeo --------------------
# Inicializamos la app flask en puerto 5000
app.run(debug=True, port=5000)
# ----------------- Fin de comentado ----------------------------------------
