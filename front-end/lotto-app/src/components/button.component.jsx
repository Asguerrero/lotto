import React from 'react';
import '../App.css';

const Button = ({children, type, ...otherProps}) => (
    <button className='main-button' type={type} {...otherProps}>
        {children}
    </button>
)

export default Button;