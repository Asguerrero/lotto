import psycopg2
import random
import flask
import json
import argparse

app = flask.Flask(__name__) 

database = 'lotto'
user ='valentinaguerrero'
password ='Perro12345678?'

@app.route('/user/create')
def create_user():
    # Get arguments from url 
    name = flask.request.args.get('name')
    phone = flask.request.args.get('phone')
    email = flask.request.args.get('email')
    password = flask.request.args.get('password')
 
    create_user_query = '''INSERT  INTO users (name, phone, email, password) VALUES (%s, %s, %s, %s) RETURNING id;'''
    connection = connect_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute(create_user_query,(name, phone, email, password, ) )
        connection.commit()
        # Fetch id of recently created user
        for row in cursor:
            user_id = row[0]
       
    except Exception as e:
        print(e)
        exit()

    return json.dumps({"user_id": user_id})

@app.route('/user/get_details')
def get_user_details():
   
    user_id = flask.request.args.get('user_id')

    get_user_details_query = '''SELECT name, email, phone FROM users WHERE id = %s;'''
    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(get_user_details_query,(user_id, ) )
        for row in cursor:
            user_details = {
                'name': row[0],
                'email': row[1],
                'phone': row[2],
            }

    except Exception as e:
        print(e)
        exit()

    return json.dumps(user_details)

@app.route('/user/get_raffles')
def get_user_raffles():
   
    user_id = flask.request.args.get('user_id')
    user_raffles = []
    get_user_raffles_query = '''SELECT id FROM raffles WHERE user_id = %s;'''
    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(get_user_raffles_query,(user_id, ) )
        for row in cursor:
            user_raffles.append(row[0])
            
    except Exception as e:
        print(e)
        exit()

    return json.dumps({'user_raffles' : user_raffles})

@app.route('/raffle/create')
def create_raffle():

    user_id = flask.request.args.get('user_id')
    drawing_date = flask.request.args.get('drawing_date')
    drawing_method = flask.request.args.get('drawing_method')
    prize = flask.request.args.get('prize')
    price = flask.request.args.get('price')
    total_tickets = flask.request.args.get('total_tickets')
    numbers_per_ticket = flask.request.args.get('numbers_per_ticket')
    style  = flask.request.args.get('style')
    payment_methods = flask.request.args.get('payment_methods').split('-')
    additional_information = flask.request.args.get('additional_information')

    create_raffle_query = '''INSERT  INTO raffles (user_id, drawing_date, drawing_method, prize, price, total_tickets, numbers_per_ticket, style, additional_information) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;'''

    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(create_raffle_query,(user_id, drawing_date, drawing_method, prize, price, total_tickets, numbers_per_ticket, style, additional_information, ) )
        connection.commit()
        for row in cursor:
            raffle_id =  row[0]
            
    except Exception as e:
        print(e)
        exit()

    # Call additional helper functions to set payment methods, create tickets and assign a number to each ticket
    create_tickets(total_tickets, raffle_id)
    create_numbers_for_tickets(raffle_id, total_tickets, numbers_per_ticket)
    set_raffle_payment_methods(raffle_id, payment_methods)

    return json.dumps({"raffle_id": raffle_id})


@app.route('/raffle/get_details')
def get_raffle_details():
    raffle_id = flask.request.args.get('raffle_id')
    raffle = get_raffle(raffle_id)
    return json.dumps(raffle)

@app.route('/raffle/get_stats')
def get_raffle_stats():
    raffle_id = flask.request.args.get('raffle_id')
    
    # Get raffle details 
    raffle = get_raffle(raffle_id)

    available_tickets = len(get_raffle_tickets_according_to_payment_status(raffle_id, 'available'))
    sold_tickets = len(get_raffle_tickets_according_to_payment_status(raffle_id, 'sold'))
    reserved_tickets = len(get_raffle_tickets_according_to_payment_status(raffle_id, 'reserved'))
    total_tickets = available_tickets + sold_tickets + reserved_tickets

    stats = {
        'sold tickets total': sold_tickets,
        'sold tickets percentage': (sold_tickets * 100)/total_tickets,
        'money from sold tickets': sold_tickets * raffle['price'],
        'reserved tickets total': reserved_tickets,
        'reserved tickets percentage': (reserved_tickets * 100)/total_tickets,
        'money from reserved tickets': reserved_tickets * raffle['price'],
        'available tickets total': available_tickets,
        'available tickets percentage': (available_tickets * 100)/total_tickets ,
        'drawing_date': raffle['drawing_date']
    }

    return json.dumps(stats)

@app.route('/raffle/get_tickets')
def get_raffle_tickets():
    raffle_id = flask.request.args.get('raffle_id')
    payment_status = flask.request.args.get('payment_status')
    
    # Get all tickets if payment status is unspecified
    if payment_status is None:
        tickets = get_all_raffle_tickets(raffle_id)
    
    # Get only tickets that match the required payment status
    else:
        tickets = get_raffle_tickets_according_to_payment_status(raffle_id, str(payment_status))
    
    return json.dumps(tickets)


@app.route('/raffle/delete')
def delete_raffle():
    raffle_id = flask.request.args.get('raffle_id')
    tickets = get_all_raffle_tickets(raffle_id)

    # Delete numbers related to all raffle's tickets
    for ticket in tickets:
        delete_ticket_numbers(ticket['id'])

    # Delete all tickets and payment methods related to the raffle as well as the raffle itself
    delete_raffle_tickets_query = '''DELETE FROM tickets WHERE raffle_id = %s'''
    delete_raffle_payment_methods_query = '''DELETE FROM raffles_payment_methods WHERE raffle_id = %s'''
    delete_raffle_query =  '''DELETE FROM raffles WHERE id = %s'''

    delete_queries = [delete_raffle_tickets_query, delete_raffle_payment_methods_query, delete_raffle_query]
    connection = connect_database()

    for delete_query in delete_queries:
        try:
            cursor = connection.cursor()
            cursor.execute(delete_query,(raffle_id, ) )
            connection.commit()
            response_status_code = 200

        except Exception as e:
            print(e)
            exit()
   
    return json.dumps({'status_code': response_status_code})

@app.route('/ticket/get_details')
def get_ticket():
    ticket_id = flask.request.args.get('ticket_id')
    ticket = get_ticket_by_id(ticket_id)
    return json.dumps(ticket)

@app.route('/ticket/make_reservation')
def make_ticket_reservation():
    ticket_id = flask.request.args.get('ticket_id')
    name = flask.request.args.get('name')
    email = flask.request.args.get('email')
    phone = flask.request.args.get('phone')

    ticket = get_ticket_by_id(ticket_id)

    # Users can only reserve tickets that are available
    if ticket['payment_status'] == 'available':
        make_reservation_query = '''UPDATE tickets SET payment_status='reserved', name = %s, email = %s, phone= %s WHERE id=%s;'''
        connection = connect_database()
    
        try:
            cursor = connection.cursor()
            cursor.execute(make_reservation_query,(name, email, phone, ticket_id,) )
            connection.commit()
            response_status_code = 200
                
        except Exception as e:
            print(e)
            exit()
    else:
        response_status_code = 400
        

    return json.dumps({'status_code': response_status_code})

@app.route('/ticket/edit')
def edit_ticket():
    ticket_id = flask.request.args.get('ticket_id')
    name = flask.request.args.get('name')
    email = flask.request.args.get('email')
    phone = flask.request.args.get('phone')
    payment_status = flask.request.args.get('payment_status')

    # Create portion of query with optional parameters
    optional_parameters = {'name': name, 'email': email, 'phone': phone, 'payment_status': payment_status}
    query_values = []

    for parameter in optional_parameters:
        if optional_parameters[parameter] is not None:
            # Example: name = 'Jhon'
            assign_paramater_to_value_string = f"{parameter} = '{optional_parameters[parameter]}'"
            query_values.append(assign_paramater_to_value_string)

    query_values = ', '.join(parameters_values)

    edit_ticket_query = '''UPDATE tickets SET {} WHERE id=%s;'''.format(query_values)
    connection = connect_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute(edit_ticket_query,(ticket_id,) )
        connection.commit()
        response_status_code = 200
            
    except Exception as e:
        print(e)
        exit()
    
    return json.dumps({'status_code': response_status_code})

@app.route('/ticket/reset')
def reset_ticket():
    ticket_id = flask.request.args.get('ticket_id')

    reset_ticket_query = '''UPDATE tickets SET name= NULL, email= NULL, phone=NULL, payment_status='available' WHERE id=%s;'''
    connection = connect_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute(reset_ticket_query,(ticket_id,) )
        connection.commit()
        response_status_code = 200
            
    except Exception as e:
        print(e)
        exit()
    
    return json.dumps({'status_code': response_status_code})

@app.route('/ticket/confirm_payment')
def confirm_ticket_payment():
    ticket_id = flask.request.args.get('ticket_id')
    ticket = get_ticket_by_id(ticket_id)
    
    # For a ticket to have 'sold' as payment status, it should have all the information about te buyer/participant
    if (ticket['name'] is not None and ticket['email'] is not None and ticket['phone'] is not None):
        confirm_payment_query = '''UPDATE tickets SET payment_status='sold' WHERE id=%s;'''
        connection = connect_database()
        
        try:
            cursor = connection.cursor()
            cursor.execute(confirm_payment_query,(ticket_id,) )
            connection.commit()
            response_status_code = 200
                
        except Exception as e:
            print(e)
            exit()
    else:
        response_status_code = 400

    
    return json.dumps({'status_code': response_status_code})

# --------- Admin functions ---------
# These functions will only be used by the admin of the application 
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
                    'winner_ticket_id': row[6],
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


# --------- Helper functions ---------

# DB function
def connect_database():
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
        return connection
    except Exception as e:
        print(e)
        exit()

# Raffle function
def get_raffle(raffle_id):
    get_raffle_query = '''SELECT * FROM raffles WHERE id = %s;'''
    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(get_raffle_query,(raffle_id, ) )
        for row in cursor:
            raffle ={
                'id': row[0],
                'user_id': row[1],
                'creation_date' : str(row[2]),
                'drawing_date': str(row[3]),
                'drawing_method': row[4],
                'prize': row[5],
                'winner_ticket_id': row[6],
                'price': row[7],
                'total_tickets': row[8],
                'numbers_per_ticket': row[9],
                'style': row[10],
                'additional_information': row[11],
                'payment_methods': get_raffle_payment_methods(raffle_id)
            }
       
    except Exception as e:
        print(e)
        exit()

    return raffle


# Tickets functions
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
                assign_number_to_ticket(ticket_id, ticket_number)
                current_number_index = current_number_index + 1
    
    except Exception as e:
        print(e)
        exit()


def assign_number_to_ticket(ticket_id, ticket_number):
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

def delete_ticket_numbers(ticket_id):
    delete_ticket_numbers_query = '''DELETE FROM tickets_numbers WHERE ticket_id = %s'''
    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(delete_ticket_numbers_query,(ticket_id, ) )
        connection.commit()

    except Exception as e:
        print(e)
        exit()

def get_ticket_by_id(ticket_id):
    get_ticket_by_id_query = '''SELECT id, raffle_id, name, phone, email, payment_status  
    FROM tickets WHERE id = %s;'''
    connection = connect_database()
    
    try:
        cursor = connection.cursor()
        cursor.execute(get_ticket_by_id_query,(ticket_id, ))
        for row in cursor:

            ticket = {
                    'id': row[0],
                    'raffle_id' : row[1],
                    'name': row[2],
                    'phone': row[3],
                    'email': row[4],
                    'payment_status': row[5],
                    'numbers': get_ticket_numbers(row[0])
            }
            
    except Exception as e:
        print(e)
        exit()

    return ticket

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


def get_all_raffle_tickets(raffle_id):
    tickets = []
    get_tickets_according_to_payment_status_query = '''SELECT tickets.id, tickets.raffle_id, tickets.name, tickets.phone, tickets.email, tickets.payment_status  
    FROM raffles, tickets WHERE raffles.id = %s AND tickets.raffle_id = raffles.id;'''
    connection = connect_database()
    try:
        cursor = connection.cursor()
        cursor.execute(get_tickets_according_to_payment_status_query,(raffle_id, ))
        for row in cursor:
            ticket_dict = {
                    'id': row[0],
                    'raffle_id' : row[1],
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

def get_raffle_tickets_according_to_payment_status(raffle_id, payment_status):
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

# Payment methods functions

def get_raffle_payment_methods(raffle_id):
    payment_methods = []
    get_raffle_payment_methods_query = '''SELECT * FROM raffles_payment_methods WHERE raffle_id = %s;'''
    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(get_raffle_payment_methods_query,(raffle_id, ) )
        for row in cursor:
            payment_method = {
                'method' : get_payment_method_name(row[1]), 
                'details': row[2]
            }
            payment_methods.append(payment_method)
           
    except Exception as e:
        print(e)
        exit()

    return payment_methods

def get_payment_method_id(payment_method):
    get_payment_method_id_query = '''SELECT * FROM payment_methods WHERE method = %s;'''
    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(get_payment_method_id_query,(payment_method, ) )
        for row in cursor:
            return row[0]
            
    except Exception as e:
        print(e)
        exit()


def get_payment_method_name(payment_method_id):
    get_payment_method_name_query = '''SELECT * FROM payment_methods WHERE id = %s;'''
    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(get_payment_method_name_query,(payment_method_id, ) )
        for row in cursor:
            return row[1]
            
    except Exception as e:
        print(e)
        exit()


def create_payment_method(payment_method):
    create_payment_method_query = '''INSERT INTO payment_methods (method) VALUES (%s);'''
    connection = connect_database()

    try:
        cursor = connection.cursor()
        cursor.execute(create_payment_method_query,(payment_method, ) )
        connection.commit()
        payment_method_id = get_payment_method_id(payment_method)
            
       
    except Exception as e:
        print(e)
        exit()
    
    return payment_method_id


def set_raffle_payment_methods(raffle_id, payment_methods):
    for method in payment_methods:
        parameters = method.split(':')
        payment_method = parameters[0].lower()
        if len(parameters) > 1:
            additional_information = parameters[1]
        else:
            additional_information= None
        payment_method_id = get_payment_method_id(payment_method)

        if payment_method_id is None:
            payment_method_id = create_payment_method(payment_method)
        
        create_entry_in_raffles_payment_methods_table = '''INSERT INTO raffles_payment_methods (raffle_id, payment_method_id, details) 
                                                        VALUES (%s, %s, %s);'''
        connection = connect_database()
        
        try:
            cursor = connection.cursor()
            cursor.execute(create_entry_in_raffles_payment_methods_table,(raffle_id, payment_method_id, additional_information, ) )
            connection.commit()
            status = cursor.statusmessage
       
        except Exception as e:
            print(e)
            exit()

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)