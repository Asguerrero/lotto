import React from 'react';
import Button from '../components/button.component';
import PaymentMethodsInfo from '../components/form-sections/payment-methods-info.component'
import Question from '../components/form-sections/basic-question.component.jsx'
import BlueTicketPreview from '../components/ticket-styles-previews/blue-ticket-preview.component'

class CreateRafflePage extends React.Component {
    constructor(){
        super();
        this.state = { 
            raffle_id: null,
            progress : 0,
            prize: '',
            additional_information_checkbox: false,
            additional_information: '',
            total_tickets: 0,
            drawing_date: '',
            drawing_method: 'default',
            external_lottery: null,
            price: 0,
            payment_methods: {},
            other_payment_method_checkbox: false,
            other_payment_method: '',
            user: {name: '', email: '', phone: ''},
            numbers_per_ticket: 1,
        };
        this.createRaffle= this.createRaffle.bind(this);
    }

    handleSubmit = event => {
        event.preventDefault();
        const {progress } = this.state;
        this.setState({ progress : progress + 1 });
    }

    handleChange = event => {
        const { name, value } = event.target;
        this.setState({ [name]: value });
    };

    handleReturn = () => {
        const {progress } = this.state;
        this.setState({ progress : progress - 1 });
       
    };

    handleAdditionalInformationCheckbox = event => {

        console.log(event.target.value);
        const { value } = event.target;

        this.setState({additional_information_checkbox: !this.state.additional_information_checkbox}, function() {
            console.log(this.state.additional_information_checkbox)});

    }

    handlePaymentMethodsCheckbox = event => {
        const { name, value } = event.target;
        const {payment_methods} = this.state;

        if(value in payment_methods){
            delete payment_methods[value]
        }
        else{
            payment_methods[value] = ''
        }
        
    }

    handleOtherPaymentMethodOption = event => {
        const { value } = event.target;
        this.setState({other_payment_method_checkbox: !this.state.other_payment_method_checkbox})
    }


    handleUserInfoChange= event => {
        const {name, value } = event.target;
        const {user} = this.state;
        user[name]= value;

    }

    shouldUseExternalLottery = () => {
       
        const total_tickets = parseInt(this.state.total_tickets)
        if(total_tickets !== 0){
            if (total_tickets <= 10){
                if (total_tickets === 5 || total_tickets === 10){ 
                    return true;
                }
                else{
                    return false;
                }
    
            }
            else if (total_tickets <= 100){
                if (total_tickets === 50 || total_tickets === 20 || total_tickets === 100 ){
                    return true;
                }
                else{
                    return false;
                }
    
            }
    
            else if (total_tickets <= 1000){
                if (total_tickets === 500 || total_tickets === 200 || total_tickets === 1000){
                    return true;
                }
                else{
                    return false;
                }
            }
    
        }
        else{
            return true;
        }
        
    }

    async createRaffle(){
        const {drawing_date, drawing_method, prize, price, total_tickets, external_lottery, numbers_per_ticket} = this.state
        const root_domain = 'http://localhost:5000'
        const cors_url = "https://cors-anywhere.herokuapp.com/";

        const response = await fetch(`${root_domain}//raffle/create?user_id=1&drawing_date=${drawing_date}&drawing_method=${drawing_method}&prize=${prize}&total_tickets=${total_tickets}&numbers_per_ticket=${numbers_per_ticket}&style=1&price=${price}&payment_methods=nequi:3214963720-cash-daviplata:18004444444`, {
            "headers": {
            'Access-Control-Allow-Origin': 'http://localhost:3000'
        }})
        const raffle_response = await response.json();
        this.setState({ raffle_id : raffle_response.raffle_id  });
    }

    
    render() {

        switch (this.state.progress ) {
            case 0 :
            return(
                <div className='flex center create-raffle-form'>
                    <form className='w-60' onSubmit={this.handleSubmit}>
                        <h2 className='form-subtitle'>Para que tu rifa sea un exito, debemos definir primero un par de detalles generales</h2>
                        <div className='flex space-between align-flex-start margin-top-5'>
                            <h3 className='form-question'>1. ¿Que vas a rifar?</h3>
                            <input className='form-input w-70' type="text" name='prize' value={this.state.prize} required onChange={this.handleChange} />
                        </div>
                        <label> Algunas personas rifan electrodomesticos o dinero, pero tu puedes ser tan creativ@ como desees!</label>
                        
        
                        <div className='flex space-between align-flex-start margin-top-6'>
                            <h3 className='form-question'>2. ¿Esta rifa es por alguna causa especifica que quieres que tu publico conozca?</h3>
                            <label className='flex checkbox'>
                                <input type="checkbox" name='additional_information_checkbox' checked={this.state.additional_information_checkbox} onChange={this.handleAdditionalInformationCheckbox} />
                                    Si
                            </label>
                            <label className='flex checkbox'>
                                <input type="checkbox" name='additional_information_checkbox' checked={!this.state.additional_information_checkbox} onChange={this.handleAdditionalInformationCheckbox} />
                                    No
                            </label>
                        </div>

                        {   this.state.additional_information_checkbox  ? 
                        <label> Cuentanos en una frase por que estás organizando esta rifa
                            <input className='form-input w-100 margin-top-2 ' type="text" name='additional_information' value={this.state.additional_information} required onChange={this.handleChange} /> 
                        </label>
                            : null }
                        <div className='w-100 flex center margin-top-5 '>
                            <Button type='submit' >Continuar</Button>
                        </div>
                    </form>
                </div>
            
            
            )

        
        case 1: 
            return(

                <div className='flex center create-raffle-form'>
                    <form className='w-60' onSubmit={this.handleSubmit}>
                        <h2 className='form-subtitle'>Excelente decision! Ahora cuentanos como quieres que se elija al ganador@ </h2>
                        <div className='flex space-between align-flex-start margin-top-3'>
                            <h3 className='form-question'>3. ¿Cuantas boletas quieres vender?</h3>
                            <input className='form-input w-50 text-align-left ' style={{paddingRight: "10px"}} type="text" name='total_tickets'  value={this.state.total_tickets} onChange={this.handleChange} />
                        </div>

                        { this.shouldUseExternalLottery() ? 
                        null
                        :
                        <label>Teniendo en cuanta la cantidad de boletas que quieres vender te recomendamos usar el sorteo personalizado de Lotto</label>
                        }

                        <div className='flex space-between align-flex-start margin-top-3'>
                            <h3 className='form-question'>4. ¿Cuando juega tu rifa?  </h3>
                            <input className='form-input w-50 ' type="date" name='drawing_date'  onChange={this.handleChange} />
                        </div>

                        <div className='flex space-between align-flex-start margin-top-3'>
                            <h3 className='form-question'>5. ¿Como se elije al ganador?</h3>
                            <select className='form-input w-50' name="drawing_method" value={this.state.drawing_method} onChange={this.handleChange}>
                                <option value="default" disabled > -- elige una opcion -- </option>
                                <option  value="External lottery">Loteria externa</option>
                                <option  value="Lotto lottery">Sorteo de Lotto</option>
                                <option  value="Other">Otro</option>
                            </select>
                        </div>

                        { this.state.drawing_method === 'External lottery' ? <Question prompt='¿Con que loteria jugará tu rifa?' name='external_lottery' value={this.state.external_lottery}  onChange={this.handleChange}/> : null}
                        { this.state.drawing_method === 'Lotto lottery' ? <label>Fantástico! Incluiremos en todas las boletas un link para que los participantes puedan acceder al sorteo de Lotto en {this.state.drawing_date}</label>: null}
                        { this.state.drawing_method === 'Other' ? <Question prompt='¿Que metodo quieres usar?' name='external_lottery' value={this.state.external_lottery}  onChange={this.handleChange}/> : null}
                        
                        <div className='w-100 flex center margin-top-5 '>
                            <Button type='button' onClick={this.handleReturn}>Atras</Button>
                            <Button type='submit'>Continuar</Button>
                        </div>
                    </form>
                </div>
            
        
            )
        case 2:
            return(

                <div className='flex center create-raffle-form'>
                    <form className='w-60' onSubmit={this.handleSubmit}>
                        <h2 className='form-subtitle'>Ya casi terminamos! Sabemos que tu rifa va a ser la sensacion asi que es hora que decidir cuanta dinero vas a recolectar</h2>
                        <div className='flex space-between align-flex-start margin-top-3'>
                            <h3 className='form-question'>6. ¿Cuanto cuesta cada boleta?</h3>
                            <input className='form-input w-50 text-align-left 'style={{paddingRight: "10px"}} type="text" name='price'  value={this.state.price} onChange={this.handleChange} />
                        </div>
                        { this.state.price === 0 ? null : 
                            <p>Despues de vender todas las boletas, recolectaras {parseFloat(this.state.total_tickets) * parseFloat(this.state.price)} COP</p>
                        }

                        <div className='form-payment-methods-grid margin-top-5'>
                            <div className='w-100'>
                                <h3 className='form-question'>7. ¿Que medios de pago quieres usar? </h3>
                                <label>  Advertencia: Esta plataforma no maneja pagos. La informacion sobre medios de pago se anadira a cada boleta para que cada concursante pague manualmente. Es responsabilidad del administrador registrar en lotto todos los pagos </label>
                            </div>
                            
                            <div>
                                <label className='flex checkbox'>
                                    <input type="checkbox" name='payment_methods' value='Nequi' onChange={this.handlePaymentMethodsCheckbox} />
                                        Nequi
                                </label>
                                <label className='flex checkbox'>
                                    <input type="checkbox" name='payment_methods' value='Daviplata'  onChange={this.handlePaymentMethodsCheckbox} />
                                        Daviplata
                                </label>
                                <label className='flex checkbox'>
                                    <input type="checkbox" name='payment_methods' value='Bank transfer' onChange={this.handlePaymentMethodsCheckbox} />
                                        Transferencia Bancaria
                                </label>
                                <label className='flex checkbox'>
                                    <input type="checkbox" name='payment_methods' value='Cash' onChange={this.handlePaymentMethodsCheckbox} />
                                        Efectivo
                                </label>
                                <label className='flex checkbox'>
                                    <input type="checkbox" name='payment_methods' value='Other' onChange={this.handleOtherPaymentMethodOption} />
                                        Otro
                                </label>


                            </div>        
                        </div>

                        {this.state.other_payment_method_checkbox === false ? null :
                            <div>
                                <h3 className='form-question'>¿Que otro medio de pago quieres usar?</h3>
                                <input className='form-input w-100 'style={{paddingRight: "10px"}} type="text" name='other_payment_method'  value={this.state.other_payment_method} onChange={this.handleChange} />
                            </div>  
                        }

                        <div className='w-100 flex center margin-top-5 '>
                            <Button type='button' onClick={this.handleReturn}>Atras</Button>
                            <Button type='submit'>Continuar</Button>
                        </div>
                    </form>
                </div>

            )

        case 3:
            return(

                <div className='flex center create-raffle-form'>
                    <form className='w-60' onSubmit={this.handleSubmit}>
                        <h2 className='form-subtitle'>Listo! Necesitamos todos los datos de cada medio de pago</h2>
                        <div>
                            <PaymentMethodsInfo payment_methods={this.state.payment_methods} />
                        </div>

                        <div className='w-100 flex center margin-top-5 '>
                            <Button type='button' onClick={this.handleReturn}>Atras</Button>
                            <Button type='submit'>Continuar</Button>
                        </div>

                    </form>
                </div>


            )

        case 4:
            return(

                <div className='flex center create-raffle-form'>
                    <form className='w-60' onSubmit={this.handleSubmit}>
                        <h2 className='form-subtitle '>Fanstastico! Lo unico que nos falta son los datos del o la responsable de la rifa que apareceran en cada boleta</h2>
                        <div className='margin-top-5'>
                            <Question prompt='Nombre:' name='name' value={this.state.user.name}  onChange={this.handleUserInfoChange}/>
                            <Question prompt='Telefono: ' name='phone' value={this.state.user.phone}  onChange={this.handleUserInfoChange}/>
                            <Question prompt='Correo electronico: '  name='email' value={this.state.user.email}  onChange={this.handleUserInfoChange}/>
                        </div>
                        <div className='w-100 flex center margin-top-5 '>
                            <Button type='button' onClick={this.handleReturn}>Atras</Button>
                            <Button type='submit'>Continuar</Button>
                        </div>
                        
                    </form>
                </div>

            )

        case 5:
            return(

                <div className='flex center create-raffle-form'>
                    <form className='w-60' onSubmit={this.handleSubmit}>
                        <h2 className='form-subtitle '>Ultimo toque... Elige el estilo que mas se ajuste a tus necesidades</h2>
                        <div className='margin-top-5'>
                        <BlueTicketPreview prize={this.state.prize}  price={this.state.price} drawing_date={this.state.drawing_date} drawing_method={this.state.drawing_method}/>
                        </div>
                        <div className='w-100 flex center margin-top-5 '>
                            <Button type='button' onClick={this.handleReturn}>Atras</Button>
                            <Button type='submit' onClick={this.createRaffle}>Continuar</Button>
                        </div>
                        
                    </form>
                </div>

            )
        case 6: 
            return(
                <div className='flex center create-raffle-form'> 
                    <h3> Felicitaciones </h3>

                    <p>{this.state.raffle_id} </p>
                </div>
                
            )
        }
    }
}


export default CreateRafflePage;