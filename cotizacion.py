import requests
from datetime import datetime

from flask import Flask, render_template, request, redirect, jsonify, url_for
from flask_cors import CORS

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/cotization', methods=['POST'])
def cotization():
    data = request.get_json()
    estimate_time_bsale = int(data['time_estimate_bsale'])
    discount_bsale = int(data['discount_bsale'])
    estimate_time_scratch = int(data['time_estimate_scratch'])
    discount_scratch = int(data['discount_scratch'])
    colaborator_bsale = cotization_bsale.value_colab_bsale(estimate_time_bsale, discount_bsale)
    cost_bsale = cotization_bsale.costs_month_bsale()
    cost_activate_bsale = cotization_bsale.costactivate_bsale()
    colaborator_scratch = cotization_from_scratch.value_colab_from_scratch(estimate_time_scratch, discount_scratch)
    cost_scratch = cotization_from_scratch.costs_from_scratch()
    cotization_data = {
        "values": {
            "values_date": get_value()[1],
            "value_dolar": get_value()[2],
            "value_UF": get_value()[0],
        },
        "cotization_one": {
            "cotization_date": data_time(),
            "cost_brute_bsale_month": round(cost_bsale),
            "cost_brute_anual_bsale": round(cost_bsale * 12),
            "cost_IVA_month": round(cost_bsale * 0.19),
            "cost_IVA_anual": round(cost_bsale * 0.19) * 12,
            "cost_IVA_incl_bsale_month": round(cost_bsale * 1.19),
            "cost_IVA_incl_bsale_anual": round(cost_bsale * 1.19),
            "cost_activation_bsale_brute": round(cost_activate_bsale),
            "cost_activation_bsale_IVA": round(cost_activate_bsale * 0.19),
            "cost_activation_bsale_IVA_incl": round(cost_activate_bsale * 1.19),
            "total_dev": round(colaborator_bsale),
            "total_cost_brute": round(cost_activate_bsale + colaborator_bsale),
            "total_iva_activation": round(cost_activate_bsale * 0.19),
            "total_cost_activation_bsale": round((cost_activate_bsale * 1.19) + colaborator_bsale),
        },
        "cotization_two": {
            "cotization_date": data_time(),
            "valor_de_colaboradores": round(colaborator_scratch),
            "server_high_traffic_month": round(cost_scratch[0]),
            "server_high_traffic_year": round(cost_scratch[0]) * 12,
            "server_high_traffic_month ": round(cost_scratch[1]),
            "server_high_traffic_year": round(cost_scratch[1] * 12),
            "total_value_scratch": round(cost_scratch[1]) + colaborator_scratch
        }
    }
    return jsonify(cotization_data)

@app.route('/date', methods=['GET'])
def data_time():
    now = datetime.now()
    current_time = now.strftime("%d/%m/%Y %H:%M:%S")
    return current_time

@app.route('/values', methods=['GET'])
def values():
    values = {
        "values": {
            "values_date": get_value()[1],
            "value_dollar": get_value()[2],
            "value_UF": get_value()[0],
        }
    }
    return jsonify(values)

def get_value():
    r = requests.get('https://mindicador.cl/api')
    valor = r.json()
    dollar = valor["dolar"]["valor"]
    uf = valor["uf"]["valor"]
    date_str = valor["uf"]["fecha"]
    date_dt = datetime.fromisoformat(date_str.replace("Z", ""))
    dollar_entire = round(dollar)
    uf_entire = round(uf)
    return uf_entire, date_dt, dollar_entire

class cotization_bsale:
    def costs_month_bsale():
        mercadoLibre = 0.7 * get_value()[0]
        webPay = 0.95 * get_value()[0]
        ecommerce = get_value()[0]
        total_month = mercadoLibre + webPay + ecommerce
        return round(total_month)
    
    def costactivate_bsale():
        uf = get_value()[0]
        mercadoLibre = 0.7 * uf
        ecommerce = uf
        activate_bsale = mercadoLibre + ecommerce
        return round(activate_bsale)
    
    def value_colab_bsale(time_estimate_bsale, discount_bsale):
        discount = discount_bsale / 100
        discount = 1 - discount
        valorhour = get_value()[0] * discount
        totalColab = valorhour * time_estimate_bsale
        return round(totalColab)


class cotization_from_scratch():
    def costs_from_scratch():
        server_low = get_value()[2] * 14
        server_high_traffic = get_value()[2] * 100
        return server_low, server_high_traffic
    
    def value_colab_from_scratch(time_estimate, discount):
        discount = discount / 100
        discount = 1 - discount
        valorhour = get_value()[0] * discount
        totalColab = valorhour * time_estimate
        return round(totalColab)

app.run(debug=True, port=5000)
