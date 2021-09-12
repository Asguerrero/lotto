import React from 'react';

const TicketPreview = ({ticketNumbers}) => (
   <div className ='ticket-preview'>
        { ticketNumbers.map(number => ( <p key={number}>{`N ${number}`}</p>))}
   </div>
    
);

export default TicketPreview;