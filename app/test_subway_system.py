import requests
import json
import time
import os

if __name__ == '__main__':
    # Sleep for 7 Seconds to allow Flask app to start
    HEADERS = {'Content-type': 'application/json'}
    time.sleep(7)

    with open('test_out.txt', 'w') as file:
        '''
        Adding Stations: 
            A Line -> ['Houston', '23', '32', '47', '53', '64', '75'], Price: 2.75
            B Line -> ['Canal', '3', '13', '33', '44', '47', '105'], Price: 4.75
            C Line -> ['Houston', '3', '32', '33', '64', '105', '75'], Price: 3.25
            N Line -> ['Canal', '18', '32', '47', '53', '59', '113'], Price: 1.75
            1 Line -> ['Houston', '23', '32', '33', '53', '69', '75'], Price: 3.50
            2 Line -> ['Spring', '3', '13', '14', '53', '69', '113'], Price: 1.50
            3 Line -> ['Spring', '14', '33', '47', '59', '64', '75'], Price: 2.75
        '''

        file.write("*** ADDING STATIONS ***" + '\n' + "\n")

        data_master = [{'name': 'A', 'stations': ['Houston', '23', '32', '47', '53', '64', '75'], "Price": "2.75"},
                       {'name': 'B', 'stations': ['Canal', '3', '13', '33', '44', '47', '105'], "Price": "4.75"},
                       {'name': 'C', 'stations': ['Houston', '3', '32', '33', '64', '105', '75'], "Price": "3.25"},
                       {'name': 'N', 'stations': ['Canal', '18', '32', '47', '53', '59', '113'], "Price": "1.75"},
                       {'name': '1', 'stations': ['Houston', '23', '32', '33', '53', '69', '75'], "Price": "3.50"},
                       {'name': '2', 'stations': ['Spring', '3', '13', '14', '53', '69', '113'], "Price": "1.50"},
                       {'name': '3', 'stations': ['Spring', '14', '33', '47', '59', '64', '75'], "Price": "2.75"}]

        for data in data_master:
            response = requests.post('http://localhost:8080/train-line', json=data, headers=HEADERS)
            file.write(response.json()['message'][0] + '\n')

        file.write("\n" + "*** TESTING ROUTES ***" + '\n' + "\n")

        '''
        Testing for Routes:
        '''

        testing_master = [('Houston', '23'), ('Canal', 'Spring'), ('Spring', '75'),
                          ('3', '113'), ('75', 'Canal'), ('14', '105'), ('13', 'FakeSt')]

        for origin, destination in testing_master:
            route_response = requests.post(f'http://localhost:8080/route?origin={origin}&destination={destination}')
            file.write(route_response.json()['message'][0] + '\n')

        '''
        Testing for Cards:
        '''

        file.write("\n" + "*** TESTING CARD ENTRY ***" + '\n' + "\n")

        cards_master = [('1234', '13.0'), ('aG2S', '14.0'), ('sda@02', '75.3'),
                        ('af@222', '113.0'), ('7532', '156.0'), ('1ad4', '0.0'), ('1234', '2.75')]

        for id_val, amount in cards_master:
            data = {'number': id_val, 'amount': amount}
            card_response = requests.post(f'http://localhost:8080/card', json=data, headers=HEADERS)
            file.write(card_response.json()['message'][0] + '\n')

        '''
        Testing for Entering:
        '''

        file.write("\n" + "*** TESTING ENTERING ENDPOINT ***" + '\n' + "\n")

        entering_master = [('Houston', '1234'), ('23', "aG2S"), ('1000', '7532'), ('105', 'af@222'), ('105', '1ad4')]

        for station, card_id in entering_master:
            data = {'card_number': card_id}
            entering_response = requests.post(f'http://localhost:8080/station/{station}/enter', json=data,
                                              headers=HEADERS)
            file.write(entering_response.json()['message'][0] + '\n')

        '''
        Testing for Exiting:
        '''

        file.write("\n" + "*** TESTING EXITING ENDPOINT ***" + '\n' + "\n")

        exiting_master = [('105', '1234'), ('3', "aG2S"), ('49', '7532'), ('59', 'af@222')]

        for station, card_id in exiting_master:
            data = {'card_number': card_id}
            exiting_response = requests.post(f'http://localhost:8080/station/{station}/exit', json=data,
                                             headers=HEADERS)
            file.write(exiting_response.json()['message'][0] + '\n')

        '''
        Close Down DB Connections
        '''

        file.write("\n" + "*** CLOSING DB CONNECTIONS ***" + '\n' + "\n")

        end_test_response = requests.post(f'http://localhost:8080/close_down')
        file.write(end_test_response.json()['message'][0] + '\n')
