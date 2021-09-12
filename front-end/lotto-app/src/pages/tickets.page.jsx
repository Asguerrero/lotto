import React from 'react';
import { useParams } from "react-router-dom";
import TicketPreview from '../components/ticket-preview.component.jsx'



const TicketsPage = () => {
    const { id } = useParams();
    const ticketsNumbers = [1,2,3,4,5,6,7,8]

  return (
    <div>
      <h1>Raffle id is {id}</h1>
      <div className='flex center tickets-page' >
      {ticketsNumbers.map( ticketNumbers =>  <TicketPreview ticketNumbers={[ticketNumbers, 1]} /> )}
      </div>
     
    </div>
  );

}


export default TicketsPage;