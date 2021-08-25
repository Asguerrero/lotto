import React from 'react';
import Button from '../components/button.component';
import PaymentMethodsInfo from '../components/form-sections/payment-methods-info.component'


class CreateRafflePage extends React.Component {
    constructor(){
        super();
        this.state = { 
            progress : 2,
            prize: '',
            additional_information_checkbox: false,
            additional_information: '',
            total_tickets: '',
            drawing_date: '',
            drawing_method: "External lottery",
            price: 0,
            payment_methods: {},
            other_payment_method_checkbox: false,
            other_payment_method: ''
        };
    }

    handleSubmit = event => {
        event.preventDefault();
        
        const {prize, additional_information, progress } = this.state;
        this.setState({ progress : progress + 1 });

        console.log('submit');

    }

    handleChange = event => {
       
        const { name, value } = event.target;
        
        this.setState({ [name]: value });
        
       
    };

    handleReturn = () => {
        
        console.log('return clicked');
        const {progress } = this.state;
        this.setState({ progress : progress - 1 }, function() {
            console.log(this.state.progress)});
        console.log('return clicked')
       
    };

    handleCheckbox = event => {

        console.log(event.target.value);
        const { value } = event.target;

        this.setState({additional_information_checkbox: !this.state.additional_information_checkbox}, function() {
            console.log(this.state.additional_information_checkbox)});

    }

    handleOtherPaymentMethodOption = event => {
        const { value } = event.target;
        this.setState({other_payment_method_checkbox: !this.state.other_payment_method_checkbox})
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
        
        console.log(payment_methods)
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
                                <input type="checkbox" name='additional_information_checkbox' checked={this.state.additional_information_checkbox} onChange={this.handleCheckbox} />
                                    Si
                            </label>
                            <label className='flex checkbox'>
                                <input type="checkbox" name='additional_information_checkbox' checked={!this.state.additional_information_checkbox} onChange={this.handleCheckbox} />
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
                            <input className='form-input w-50' type="text" name='total_tickets'  value={this.state.total_tickets} onChange={this.handleChange} />
                        </div>

                        <div className='flex space-between align-flex-start margin-top-3'>
                            <h3 className='form-question'>4. ¿Cuando juega tu rifa?  </h3>
                            <input className='form-input w-50' type="date" name='drawing_date'  onChange={this.handleChange} />
                        </div>

                        <div className='flex space-between align-flex-start margin-top-3'>
                            <h3 className='form-question'>5. ¿Como se elije al ganador?</h3>
                            <select className='form-input w-50' name="drawing_method" value={this.state.drawing_method} onChange={this.handleChange}>
                                <option  value="External lottery">Loteria externa</option>
                                <option  value="Lotto lottery">Sorteo de Lotto</option>
                                <option  value="Other">Otro</option>
    
                            </select>
                        </div>



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
        }
    }
}


export default CreateRafflePage;