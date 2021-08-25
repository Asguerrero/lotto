import React from 'react';
import '../App.css';
import { Link } from 'react-router-dom';
import logo from '../assets/logo.png'; 

const Header = () => (
    <div className='header-container'>
        <Link className='flex center' to='/'>
            <img className='logo' src={logo} alt="Logo" />
        </Link>
        <div className='header-options-container'>
            <Link className='option' to='/shop'>
                Nosotros
            </Link>

            <Link className='option' to='/shop'>
                FAQ
            </Link>

            <Link className='option' to='/shop'>
                Donaciones
            </Link>
        </div>

        <div className='header-sign-in-container'>
            <Link className='option' to='/shop'>
                Ingresar
            </Link>
            <span className='sign-in-separator'>|</span>
            <Link className='option' to='/shop'>
                Nueva cuenta
            </Link>
        </div>
        
    </div>
)

export default Header;