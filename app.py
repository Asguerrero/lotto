import psycopg2
import random
import flask
import json
import argparse

app = flask.Flask(__name__) 

database = 'lotto'
user ='valentinaguerrero'
password ='Perro12345678?'


def connect_database():
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
        return connection
    except Exception as e:
        print(e)
        exit()

def create_tickets(total_tickets, raffle_id):
    connection = connect_database()
    create_tickets_query = '''INSERT  INTO tickets (raffle_id, payment_status) 
    VALUES (%s, %s);'''

    for ticket in range(int(total_tickets)):
        try:
            cursor = connection.cursor()
            cursor.execute(create_tickets_query, (raffle_id, 'available',))
            connection.commit()
            
        except Exception as e:
            print(e)
            exit()

def create_numbers_for_tickets(raffle_id, total_tickets, numbers_per_ticket):
    connection = connect_database()
    get_tickets_id_query = '''SELECT id FROM tickets WHERE raffle_id = %s '''

    try:
        random_numbers = create_random_numbers_array(total_tickets, numbers_per_ticket)
        current_number_index = 0
        cursor = connection.cursor()
        cursor.execute(get_tickets_id_query, (raffle_id, ))
        for ticket in cursor:
            ticket_id = ticket[0]
            for number in range(int(numbers_per_ticket)):
                ticket_number = random_numbers[current_number_index] 
                create_number_for_ticket(ticket_id, ticket_number)
                current_number_index = current_number_index + 1
    
    except Exception as e:
        print(e)
        exit()


def create_number_for_ticket(ticket_id, ticket_number):
    create_ticket_number_query = '''INSERT INTO tickets_numbers (ticket_id, ticket_number) 
    VALUES (%s, %s);'''
    connection = connect_database()
    try:
        cursor = connection.cursor()
        cursor.execute(create_ticket_number_query, (ticket_id, ticket_number, ))
        connection.commit()
    except Exception as e:
        print(e)
        exit()


def create_random_numbers_array(total_tickets, numbers_per_ticket):
    random_numbers = list(range(int(total_tickets) * int(numbers_per_ticket)))
    random.shuffle(random_numbers)
    return random_numbers

def get_ticket_numbers(ticket_id):
    ticket_numbers = []
    get_ticket_numbers_query = '''SELECT ticket_number FROM tickets_numbers WHERE ticket_id = %s;'''
    connection = connect_database()
    try:
        cursor = connection.cursor()
        cursor.execute(get_ticket_numbers_query,(ticket_id, ))
        for row in cursor:
            ticket_numbers.append(row[0])
            
    except Exception as e:
        print(e)
        exit()

    return ticket_numbers

def get_tickets_according_to_payment_status(raffle_id, payment_status):
    tickets = []
    get_tickets_according_to_payment_status_query = '''SELECT tickets.id, tickets.raffle_id, tickets.name, tickets.phone, tickets.email, tickets.payment_status  
    FROM raffles, tickets WHERE raffles.id = %s AND tickets.payment_status = %s AND tickets.raffle_id = raffles.id;'''
    connection = connect_database()
    try:
        cursor = connection.cursor()
        cursor.execute(get_tickets_according_to_payment_status_query,(raffle_id, payment_status, ))
        for row in cursor:

            ticket_dict = {
                    'id': row[0],
                    "raffle_id" : row[1],
                    'name': row[2],
                    'phone': row[3],
                    'email': row[4],
                    'payment_status': row[5],
                    'numbers': get_ticket_numbers(row[0])
            }
            tickets.append(ticket_dict)
            
    except Exception as e:
        print(e)
        exit()

    return tickets


@app.route('/raffle/create')
def create_raffle():
    raffle_id = ''
    # /raffle/create?user_id=56&drawing_date=2019-06-23&drawing_method=external&prize=smarthphone&total_tickets=10&numbers_per_ticket=2&style=1&payment_method=DaviPlata&price=90000
    user_id = flask.request.args.get('user_id')
    drawing_date = flask.request.args.get('drawing_date')
    drawing_method = flask.request.args.get('drawing_method')
    prize = flask.request.args.get('prize')
    price = flask.request.args.get('price')
    total_tickets = flask.request.args.get('total_tickets')
    numbers_per_ticket = flask.request.args.get('numbers_per_ticket')
    style  = flask.request.args.get('style')
    payment_method = flask.request.args.get('payment_method')

    connection = connect_database()
    create_raffle_query = '''INSERT  INTO raffles (user_id, drawing_date, drawing_method, prize, price, total_tickets, numbers_per_ticket, style, payment_method) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'''

    get_new_raffle_id_query = '''SELECT id FROM raffles WHERE user_id = %s AND drawing_date = %s AND drawing_method = %s AND prize = %s AND price = %s AND total_tickets = %s 
    AND numbers_per_ticket = %s AND style = %s AND payment_method = %s ;'''

    try:
        cursor = connection.cursor()
        cursor.execute(create_raffle_query,(user_id, drawing_date, drawing_method, prize, price, total_tickets, numbers_per_ticket, style, payment_method, ) )
        connection.commit()
        cursor.execute(get_new_raffle_id_query, (user_id, drawing_date, drawing_method, prize, price, total_tickets, numbers_per_ticket, style, payment_method, ))
        for row in cursor:
            raffle_id =  row[0]
            
    except Exception as e:
        print(e)
        exit()

    create_tickets(total_tickets, raffle_id)
    create_numbers_for_tickets(raffle_id, total_tickets, numbers_per_ticket)

    return json.dumps({"raffle_id": raffle_id})


@app.route('/raffle/get_details')
def raffle_get_details():
    # /raffle/get_details?raffle_id=1
    raffle_id = flask.request.args.get('raffle_id')
    get_raffle_query = '''SELECT * FROM raffles WHERE id = %s;'''
    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(get_raffle_query,(raffle_id, ) )
        for row in cursor:
            raffle_details ={
                'id': row[0],
                'user_id': row[1],
                'creation_date' : str(row[2]),
                'drawing_date': str(row[3]),
                'drawing_method': row[4],
                'prize': row[5],
                'winner': row[6],
                'price': row[7],
                'total_tickets': row[8],
                'numbers_per_ticket': row[9],
                'style': row[10],
            }
       
    except Exception as e:
        print(e)
        exit()

    return json.dumps(raffle_details)


@app.route('/raffle/get_available_tickets')
def raffle_get_available_tickets():
    raffle_id = flask.request.args.get('raffle_id')
    available_tickets = get_tickets_according_to_payment_status(raffle_id, 'available')
    return json.dumps(available_tickets)

@app.route('/raffle/get_sold_tickets')
def raffle_get_sold_tickets():
    raffle_id = flask.request.args.get('raffle_id')
    sold_tickets = get_tickets_according_to_payment_status(raffle_id, 'sold')
    return json.dumps(sold_tickets)

@app.route('/raffle/get_reserved_tickets')
def raffle_get_reserved_tickets():
    raffle_id = flask.request.args.get('raffle_id')
    reserved_tickets = get_tickets_according_to_payment_status(raffle_id, 'reserved')
    return json.dumps(reserved_tickets)


@app.route('/raffle/get_stats')
def raffle_get_stats():
    # /raffle/get_details?raffle_id=1
    raffle_id = flask.request.args.get('raffle_id')
    tickets_sold = 0
    tickets_reserved = 0
    tickets_available = 0
    get_tickets_according_to_payment_status_query = '''SELECT COUNT (tickets.id) FROM raffles, tickets WHERE raffles.id = %s AND tickets.payment_status = %s AND tickets.raffle_id = raffles.id;'''
    connection = connect_database()

    # sold, reserved and available 
    # money collected from sold tickets
    # money that could be collected from reserved tickets
    # raffle date

    try:
        cursor = connection.cursor()
        cursor.execute(get_tickets_according_to_payment_status_query,(raffle_id, 'available', ) )
        for row in cursor:
            tickets_available = row[0]
        
       
    except Exception as e:
        print(e)
        exit()

    stats = {
        'N of sold tickets': tickets_sold,
        "'%' of sold tickets": tickets_sold,
        'N of reserved tickets': tickets_reserved,
        "'%' of reserved tickets": tickets_sold,
        'N of available tickets': tickets_available,
        "'%' of available tickets": tickets_available ,
        
    }

    return json.dumps('works')



@app.route('/user/create')
def create_user():
    # /user/create?name=Sol_Camila&email=valentinaguerrero.as@hotmail.com&password=1234&phone=32124572389
    name = flask.request.args.get('name')
    phone = flask.request.args.get('phone')
    email = flask.request.args.get('email')
    password = flask.request.args.get('password')
 
    connection = connect_database()
    create_user_query = '''INSERT  INTO users (name, phone, email, password) VALUES (%s, %s, %s, %s);'''

    success_message = {
        'message' : 'records inserted successfully into database',
        'status': 200
    }

    try:
        cursor = connection.cursor()
        cursor.execute(create_user_query,(name, phone, email, password, ) )
        connection.commit()
       
    except Exception as e:
        print(e)
        exit()

    return json.dumps(success_message)


@app.route('/users/get_all')
def get_all_users():
    users = []
    connection = connect_database()
    query = '''SELECT * FROM {};'''.format('users')

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            users.append([row[0], row[1], row[2], row[3], row[4]])

    except Exception as e:
        print(e)
        exit()

    return json.dumps(users)

@app.route('/raffles/get_all')
def get_all_raffles():
    raffles = []
    connection = connect_database()
    query = '''SELECT * FROM raffles;'''

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            raffles_dict = {
                    'id': row[0],
                    "user_id" : row[1],
                    "creation_date": str(row[2]),
                    'drawing_date': str(row[3]),
                    'drawing_method': row[4],
                    'prize': row[5],
                    'winner': row[6],
                    'price': row[7],
                    'total_tickets': row[8],
                    'numbers_per_ticket': row[9],
                    'style': row[10],
                    'payment_method': row[11]

            }
            raffles.append(raffles_dict)

    except Exception as e:
        print(e)
        exit()

    return json.dumps(raffles)

@app.route('/tickets/get_all')
def get_all_tickets():
    tickets = []
    connection = connect_database()
    query = '''SELECT * FROM tickets;'''

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            ticket_dict = {
                    'id': row[0],
                    "raffle_id" : row[1],
                    'name': row[2],
                    'phone': row[3],
                    'email': row[4],
                    'payment_status': row[5]
            }
            tickets.append(ticket_dict)

    except Exception as e:
        print(e)
        exit()

    return json.dumps(tickets)

@app.route('/tickets_numbers/get_all')
def get_all_numbers():
    tickets_numbers = []
    connection = connect_database()
    query = '''SELECT * FROM tickets_numbers;'''

    try:
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor:
            numbers_dict = {
                    'ticket_id': row[0],
                    "ticket_number" : row[1],
                    
            }
            tickets_numbers.append(numbers_dict)

    except Exception as e:
        print(e)
        exit()

    return json.dumps(tickets_numbers)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)