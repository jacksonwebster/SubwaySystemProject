# Subway System Project

#### Flask application that allows users to input subway lines with stations, find optimal route between stations, create new subway cards with a given balance, and simulate entering and exiting a subway station. The API is implemented with Python3 and uses the Flask framework. Docker and Postgresql are used to maintain database and host the api. 

## Installation

1. Clone the repository to local machine
2. Install Docker and Docker Compose
3. Navigate to /SubwaySystemProject
4. To Run: _docker-compose up --build_
5. To view database: 
    - Navigate to http://localhost:8888
      - System: PostgreSQL
      - Username: postgres
      - Password: password
      - DB: subway

## Usage

The API (/app/subway_flask_api.py) exposes the following endpoints:

- /train-line (POST): Creates a new train line given name, stations, price
- /route (POST): Get route between origin and destination stations (BFS)
- /card (POST):  Create new card with ID and amount
- /station/<station>/enter (POST): Enter Station, deduct price from card number
- /station/<station>/exit (POST): Exit Station, return value of card number
- /close_down (POST): Ends the testing suite and closes the database connection.

## Implementation

The implementation of the SubwaySystem class can be found in the subway_system.py file. The class initializes the database connection, creates the tables, and implementing the functions referenced by the flask api. 

## Dependencies

- Flask (1.1.2)
- pg8000 (1.21.2)

## Testing
The testing suite is found in test_subway_system.py. This suite is conducted when calling _docker-compose up --build_, and makes requests to each API endpoint. The results of these calls are written in /app/test_out.txt

The API uses a PostgreSQL database to record and update information on the subway system and users. The db is hosted in a separate docker container identified by service db. The API and testing suite are hosted in app. 