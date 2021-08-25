import React from 'react';
import Question from './basic-question.component.jsx'

const PaymentMethodsInfo = ({payment_methods}) => (

    <div>
    { Object.keys(payment_methods).map(key => {
        
            if (key === 'Daviplata' || key === 'Nequi'){
                return(
                    <div key={`${key}_div`}>
                        <h3 className='form-subtitle margin-top-3' style={{fontSize: '1.2rem'}}>{key}</h3>
                        <Question prompt={`Numero de telefono asociado a ${key}`} />
                    </div>
                )
            }
            else if(key === 'Bank transfer'){
                return(
                    <div key={`${key}_div`}>
                        <h3 key={key} className='form-subtitle margin-top-3' style={{fontSize: '1.2rem'}}>Transferencia bancaria</h3>
                        <Question prompt={'Numero de cuenta bancaria'} />
                        <Question prompt={'Nombre del titular'} />
                        <Question prompt={'Documento de identificacion'} />
                    </div>
                )
            }
            else{
                return( null)
            }
        }
       
       
       )}
    </div>
    
)

export default PaymentMethodsInfo;