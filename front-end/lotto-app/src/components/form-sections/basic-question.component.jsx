import React from 'react';


const Question = ({prompt, ...otherProps}) => (
    <div className='flex space-between align-flex-start margin-top-3' key={`${prompt}_div`}>
            <h3 className='form-payment-info' key={prompt}>{prompt}</h3>
            <input className='form-input w-50' key={`${prompt}_input`} type="text" {...otherProps}/>
    </div>

)

export default Question;