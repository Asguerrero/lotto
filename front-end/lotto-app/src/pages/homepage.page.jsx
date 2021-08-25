import React from 'react';
import Button from '../components/button.component'

const HomePage = () => (
    <div >
        <div className='margin-top-8'>
            <h1 className='text-center gray-title'>DIGITALIZA TUS RIFAS Y ENFOCATE EN LO QUE MAS IMPORTA</h1>
            <div className='flex center '>
                <div className='w-50 flex space-evenly margin-top-8'>
                    <Button>Crear nueva rifa</Button>
                    <Button>Ya tengo una cuenta</Button>
                </div>
            </div>
        </div>

        <div className='gray margin-top-8'>
            <h2 className='text-center gray-title'>¿Comó funciona?</h2>
                <div className='how-it-works-grid'>
                    <div className=' how-it-works-item'>
                        <div className='circle how-it-works-item'></div>
                        <p>1. Crea una rifa que se ajuste a tus necesidades</p>
                    </div>

                    <div className=' how-it-works-item'>
                        <div className='circle'></div>
                        <p>2. Compartela y promocionala con tu publico</p>
                    </div>

                    <div className=' how-it-works-item'>
                        <div className='circle how-it-works-item'></div>
                        <p>3. Maneja tus ventas y alcanza todas tus metas</p>
                    </div>
                </div>
                
            
        </div>
    </div>
);

export default HomePage;