from flask import Flask, request, jsonify
from subway_system import SubwaySystem

app = Flask(__name__)

# Create New Instance of Subway System and Initialize DB Connection
subway_system = SubwaySystem()
subway_system.initialize_system()

'''
FLASK ENDPOINTS
'''


# Create Train Line with name, stations, price
@app.route('/train-line', methods=['POST'])
def create_train_line():
    data = request.get_json()
    name = data['name']
    stations = data['stations']
    price = data['Price']
    response = subway_system.create_train_line(name, stations, price)
    return jsonify({'message': [response]})


# Get route between origin and destination stations (BFS)
@app.route('/route', methods=['POST'])
def get_route():
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    route = subway_system.get_optimal_route(origin, destination)

    if route:
        return jsonify({'message': [route]})

    else:
        return jsonify({'message': [f'Cannot find a route from {origin} to {destination}']})


# Create new card with ID and amount
@app.route('/card', methods=['POST'])
def create_card():
    data = request.get_json()
    number = data['number']
    amount = data['amount']
    response = subway_system.create_card(number, amount)
    return jsonify({'message': [response]})


# Enter Station, deduct price from card number
@app.route('/station/<station>/enter', methods=['POST'])
def enter_station(station):
    data = request.get_json()
    card_number = data['card_number']
    response = subway_system.enter_station(station, card_number)
    return jsonify({'message': [response]})


# Exit Station, return value of card number
@app.route('/station/<station>/exit', methods=['POST'])
def exit_station(station):
    data = request.get_json()
    card_number = data['card_number']
    response = subway_system.exit_station(station, card_number)
    return jsonify({'message': [response]})


# End testing suite, close DB connection
@app.route('/close_down', methods=['POST'])
def end_tests():
    subway_system.close_system()
    return jsonify({'message': ["Subway Instance Closed"]})


# Begin flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
