import React from 'react';

const ProgressBar = ({progress}) => (
    <div className='w-100 center flex'>
        <progress className='progress-bar' id="file" value={progress} max="100">{progress}% </progress>
    </div>

)


export default ProgressBar;