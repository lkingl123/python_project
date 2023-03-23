from DBbaseproject import HotelDB

db = HotelDB('hoteldb.sqlite')

def make_reservation():
    print('Make a reservation')
    start_date = input('Enter start date (YYYY-MM-DD): ')
    end_date = input('Enter end date (YYYY-MM-DD): ')
    available_rooms = db.get_available_rooms(start_date, end_date)
    if not available_rooms:
        print('Sorry, no rooms available for the selected dates.')
        return
    print('Available rooms:')
    for room in available_rooms:
        print(f'{room[0]}: Room {room[1]} ({room[2]}) - ${room[3]} per night')
    room_id = input('Enter room ID: ')
    guest_name = input('Enter guest name: ')

    db.add_reservation(room_id, guest_name, start_date, end_date)
    print(f'Reservation for Room {room_id} ({guest_name}, {start_date} - {end_date}) created successfully!')

def add_guest():
    print('Add a guest')
    guest_name = input('Enter guest name: ')
    guest_email = input('Enter guest email: ')
    db.add_guest(guest_name, guest_email)
    print(f'Guest {guest_name} with email {guest_email} added successfully!')


def main():
    while True:
        print('Welcome to Hotel Reservation System')
        print('1. Make a reservation')
        print('2. Add a guest')
        print('3. Exit')
        choice = input('Enter your choice: ')
        try:
            choice = int(choice)
        except Exception as e:
            print('Invalid choice. Please enter a number.', e)
            continue
        if choice == 1:
            make_reservation()
        elif choice == 2:
            add_guest()
        elif choice == 3:
            print("Thank you for using Hotel Reservation System!")
            break
        else:
            print('Invalid choice. Please enter 1, 2, or 3.')

if __name__ == '__main__':
    main()
    db.close()
