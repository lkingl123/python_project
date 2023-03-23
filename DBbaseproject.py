import sqlite3
import csv

class Guest:
    def __init__(self, name, email):
        self.name = name
        self.email = email

#connect to database

class HotelDB:

    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.create_tables()
        except Exception as e:
            print(f"Error connecting to database: {str(e)}")

#Creating a seperate place for creating tables

    def create_tables(self):
        try:
            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS rooms (
                        id INTEGER PRIMARY KEY,
                        types TEXT,
                        room_number INTEGER UNIQUE,
                        room_type TEXT,
                        price REAL,
                        is_available BOOLEAN
                    )
                ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS reservations (
                        id INTEGER PRIMARY KEY,
                        room_id INTEGER,
                        guest_name TEXT,
                        start_date TEXT,
                        end_date TEXT,
                        FOREIGN KEY (room_id) REFERENCES rooms (id)
                    )
                ''')

            self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS guests (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        email TEXT UNIQUE
                    )
                ''')

            self.conn.commit()
        except Exception as e:
            print(f"Error creating tables: {str(e)}")

#adding rooms function

    def add_room(self, room_type, room_number, price, is_available):
        try:
            self.cursor.execute('''
                INSERT INTO rooms (room_type, room_number, price, is_available)
                VALUES (?, ?, ?, ?)
            ''', (room_type, room_number, price, is_available))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding room: {str(e)}")

#adding reservation function

    def add_reservation(self, room_id, guest_name, start_date, end_date):
        try:
            self.cursor.execute('''
                INSERT INTO reservations (room_id, guest_name, start_date, end_date)
                VALUES (?, ?, ?, ?)
            ''', (room_id, guest_name, start_date, end_date))
            self.conn.commit()
        except Exception as e:
            print(f"Error adding reservation: {str(e)}")

#getting available rooms function

    def get_available_rooms(self, start_date, end_date):
        try:
            self.cursor.execute('''
                SELECT r.id, r.room_number, r.room_type, r.price
                FROM rooms r
                WHERE r.is_available = 1 AND r.id NOT IN (
                    SELECT room_id FROM reservations
                    WHERE start_date <= ? AND end_date >= ?
                )
            ''', (end_date, start_date))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error retrieving available rooms: {str(e)}")

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print(f"Error closing database connection: {str(e)}")

#created a reset function for test purposes

    def reset_database(self):
        self.cursor.execute('DROP TABLE IF EXISTS reservations')
        self.cursor.execute('DROP TABLE IF EXISTS rooms')
        self.conn.commit()
        print("Reset Successful")


    def populate_from_csv(self, csv_file):
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['type'] == 'room':
                    self.add_room(row['room_type'], int(row['room_number']), float(row['price']),
                                  bool(row['is_available']))
                elif row['type'] == 'reservation':
                    if 'id' not in row:
                        print("No id found for reservation")
                        continue
                    room_id = self.get_available_rooms(row['start_date'], row['end_date'])
                    if not room_id:
                        print(f"No available rooms found for reservation {row['id']}")
                        continue
                    room_id = room_id[0][0]
                    self.add_reservation(room_id, row['guest_name'], row['start_date'], row['end_date'])

    def add_guest(self, guest_name, guest_email):
        try:
            self.cursor.execute('''
                INSERT INTO guests (name, email)
                VALUES (?, ?)
            ''', (guest_name, guest_email))
            self.conn.commit()
            return self.cursor.lastrowid
        except Exception as e:
            print(f"Error adding guest: {str(e)}")
            return None

    def get_guest(self, guest_id):
        try:
            self.cursor.execute('SELECT * FROM guests WHERE id = ?', (guest_id,))
            row = self.cursor.fetchone()
            if row:
                return Guest(row[1], row[2])
            else:
                return None
        except Exception as e:
            print(f"Error getting guest: {str(e)}")
            return None

    def update_guest(self, guest):
        try:
            self.cursor.execute('UPDATE guests SET name = ?, email = ? WHERE id = ?',
                                (guest.name, guest.email, guest.id))
            self.conn.commit()
        except Exception as e:
            print(f"Error updating guest: {str(e)}")

    def delete_guest(self, guest_id):
        try:
            self.cursor.execute('DELETE FROM guests WHERE id = ?', (guest_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting guest: {str(e)}")


if __name__ == '__main__':
    db = HotelDB('hoteldb.sqlite')
    db.populate_from_csv('rooms.csv')
    # db.reset_database()
    db.close()

