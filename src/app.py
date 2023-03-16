from flask import Flask, make_response, request

from productionplan.powerplant import Prices, PowerPlant, apply

app = Flask(__name__)


@app.route('/')
def health_check():  # put application's code here
    return make_response({'status': 'OK'}, 200)


@app.route('/productionplan', methods=['POST'])
def production_plan():
    payload = request.json
    expected_load = int(payload['load'])
    raw_prices = payload['fuels']
    parsed_prices = {key.partition('(')[0]: value for key, value in raw_prices.items()}
    prices = Prices(**parsed_prices)
    plants = []
    for raw_plant in payload['powerplants']:
        plant = PowerPlant.from_raw(**raw_plant, prices=prices)
        plants.append(plant)
    result = apply(expected_load, plants)
    return make_response(result, 200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888, debug=True)
