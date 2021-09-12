import React from 'react';

const BlueTicketPreview = ({prize, price, user, payment_methods, drawing_date, drawing_method, additionaL_information}) => (
    <div className='blue-ticket-div'>
        <div className='blue-ticket-grid'>
            <div className='blue-ticket-background '>
                <h2>{prize.toUpperCase()}</h2>
                <h3>{`$${price}`}</h3>
            </div>

            <div className='blue-ticket-general-info'>
                <p>Juega el {drawing_date} con las ultimas dos cifras de {drawing_method}</p>

                <p>Metodos de pago aceptados:</p>
            </div>
        </div>

        <div className='blue-ticket-participant-info'>
            <p>Nombre:</p>
            <p>Email:</p>
            <p>Telefono:</p>
            <div className='blue-ticket-number'> <p className='text-center'>N 31</p></div>

        </div>

    </div>
);


export default BlueTicketPreview;