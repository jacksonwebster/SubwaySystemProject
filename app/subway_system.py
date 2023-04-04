import pg8000
from collections import deque


class SubwaySystem:
    cur, conn = None, None

    def initialize_system(self):
        # Connect to the PostgreSQL database
        self.conn = pg8000.connect(
            user='postgres',
            password='password',
            host='db',
            port=5432,
            database='subway'
        )
        self.cur = self.conn.cursor()

        print("DATABASE CONNECTION ESTABLISHED")

        # Create train line table
        self.cur.execute("CREATE TABLE IF NOT EXISTS train_line (id SERIAL PRIMARY KEY, name TEXT, price FLOAT);")
        self.conn.commit()

        print("TRAIN LINE TABLE CREATED")

        # Create station table
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS station (id SERIAL PRIMARY KEY, name TEXT, line_id INTEGER REFERENCES "
            "train_line(id));")
        self.conn.commit()

        print("STATION TABLE CREATED")

        # Create card table
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS card (id TEXT PRIMARY KEY, balance FLOAT);")
        self.conn.commit()

        print("CARD TABLE CREATED")

        # Create ride table
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS ride (id SERIAL PRIMARY KEY, card_number TEXT REFERENCES card(id), "
            "station_id INTEGER REFERENCES station(id));")
        self.conn.commit()

        print("RIDE TABLE CREATED")

    def close_system(self):
        self.conn.close()
        self.cur.close()

    def create_train_line(self, name, stations, price):
        # Enter new train line with given name
        self.cur.execute("INSERT INTO train_line (name, price) VALUES (%s, %s)", (name, price))
        self.conn.commit()

        # Retrieve id of new train line
        self.cur.execute("SELECT id FROM train_line ORDER BY id DESC LIMIT 1;")
        line_id = self.cur.fetchone()[0]

        # For each station, add to station table with name and line_id from new train line
        for station_name in stations:
            self.cur.execute("INSERT INTO station (name, line_id) VALUES (%s, %s)", (station_name, line_id))
        self.conn.commit()

        return f"Train line {name} created with stations {', '.join(stations)} and price {price}"

    def create_card(self, id_val, amount):
        # Attempt to select card
        self.cur.execute("SELECT balance FROM card WHERE id = %s", (id_val,))
        result = self.cur.fetchone()

        # Enter new card or update value
        if result is None:
            self.cur.execute("INSERT INTO card (id, balance) VALUES (%s, %s)", (id_val, float(amount),))
            new_amount = float(amount)
        else:
            new_amount = result[0] + float(amount)
            self.cur.execute("UPDATE card SET balance = %s WHERE id = %s", (new_amount, id_val,))

        self.conn.commit()

        return f"Card {id_val} has balance: {new_amount}"

    def enter_station(self, station, id_val):
        # Attempt to find card
        self.cur.execute("SELECT balance FROM card WHERE id = %s", (id_val,))
        card_result = self.cur.fetchone()

        if card_result is None:
            return "Card ID Invalid"

        # Attempt to find line_id
        self.cur.execute("SELECT line_id from station WHERE name = %s", (station,))
        line_result = self.cur.fetchone()

        if line_result is None:
            return "Station not Found"

        else:
            # Find price and update if sufficient fare
            self.cur.execute("SELECT price from train_line WHERE id = %s", (line_result[0],))
            price_result = self.cur.fetchone()

            new_balance = card_result[0] - price_result[0]

            if new_balance < 0:
                return "Insufficient Fare"

            else:
                # Record ride in ride table, update card balance
                self.cur.execute("INSERT INTO ride (card_number, station_id) VALUES (%s, %s)",
                                 (id_val, line_result[0],))
                self.conn.commit()
                self.cur.execute("UPDATE card SET balance = %s WHERE id = %s", (new_balance, id_val,))
                self.conn.commit()
                return f"Card {id_val} now has balance: {new_balance}"

    def exit_station(self, station, id_val):
        # Find current balance of card

        self.cur.execute("SELECT balance FROM card WHERE id = %s", (id_val,))
        card_result = self.cur.fetchone()

        if card_result is None:
            return "Card ID Invalid"

        # Verify station
        self.cur.execute("SELECT name from station where name = %s", (station,))
        name_result = self.cur.fetchone()
        if name_result is None:
            return "Station not Found"

        else:
            # Return card balance (No transaction upon exit - Can change)
            return f"Card {id_val} has balance: {card_result[0]}"

    def get_optimal_route(self, origin, destination):
        """
        :param origin: Name of Origin Station
        :param destination: Name of Destination Station
        :return: Route from Origin to Destination or Failure

        BFS: Beginning with origin station, find neighbors which share the same line (23,56...) or same name on
        different line. At each step, add new neighbors and record previous station. When destination is reached,
        backtrack to find the shortest route to destination.
        """

        self.cur.execute("SELECT id, line_id FROM station WHERE name = %s", (origin,))
        origin_id, origin_line_id = self.cur.fetchone()

        queue = deque([(origin, origin_id, origin_line_id)])
        seen = set()
        previous = {}

        while queue:
            cur_name, cur_id, cur_line_id = queue.popleft()

            # Destination Found
            if cur_name == destination:
                path = []
                while cur_name != origin:
                    path.append(cur_name)
                    cur_name, cur_id = previous[(cur_name, cur_id)]

                path.append(origin)
                path.reverse()
                return f'Optimal route from {origin} to {destination}: {path}'

            """
            Queue for neighbors:
            
            All neighbors with same name on different train lines 
            One neighbor ahead on current trainline: WHERE id > curID
            One neighbor behind on current trainline: WHERE id< curID
            
            """
            self.cur.execute(
                """
                (
                SELECT name, id, line_id FROM station WHERE id != %s AND name = %s AND line_id != %s
                )
                UNION
                (
                SELECT name, id, line_id FROM station WHERE id != %s 
                AND line_id = %s AND id > %s ORDER BY id ASC LIMIT 1
                )
                UNION
                (
                SELECT name, id, line_id FROM station WHERE id != %s 
                AND line_id = %s AND id < %s ORDER BY id DESC LIMIT 1
                )
                """
                ,
                (cur_id, cur_name, cur_line_id, cur_id, cur_line_id, cur_id, cur_id, cur_line_id, cur_id)
            )

            neighbors = [(row[0], row[1], row[2]) for row in self.cur.fetchall()]

            for neighbor in neighbors:
                if neighbor[1] not in seen:
                    queue.append(neighbor)
                    previous[(neighbor[0], neighbor[1])] = (cur_name, cur_id)
                    seen.add(neighbor[1])

        return None
