CREATE TABLE users(
    id  SERIAL,
    name text,
    email text,
    phone text,
    password text
);

CREATE TABLE raffles(
	id SERIAL,
	user_id integer,
	creation_date DATE NOT NULL DEFAULT CURRENT_DATE,
	drawing_date date,
    drawing_method text,
	prize text,
    winner text,
    price integer,
    total_tickets integer,
    numbers_per_ticket integer,
	style integer
);


CREATE TABLE tickets(
	id SERIAL,
	raffle_id integer,
    name integer, 
	phone text,
	email text,
	payment_status text
	
);

CREATE TABLE tickets_numbers(
    ticket_id integer,
    ticket_number integer
);

CREATE TABLE payment_method{
    id SERIAL,
    method text,
}

CREATE TABLE raffles_payment_methods{
    raffle_id integer,
    payment_method integer
}