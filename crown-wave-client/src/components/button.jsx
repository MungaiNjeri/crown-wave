import React from "react";
import PropTypes from "prop-types";
import './comp-styles/button.css'

function Button({
    type = "text",
    placeholder = "",
    onClick,
    error,
    className = "",
    ...rest
  }){
    return(

        <div className={`submit-wrapper ${className}`}>
            <button
            type={type}
            placeholder = ''
            //onClick={handlesubmit}
            className={`submit-button ${error ? "input-error" : ""}`}
            {...rest}
            >{placeholder}</button>
            {error && <small className="error-message">{error}</small>}
      </div>
    )

}

Button.propTypes = {

    type: PropTypes.string,
    placeholder: PropTypes.string,
    //onClick: PropTypes.func.isRequired,
    error: PropTypes.string,
    className: PropTypes.string,
  };



export default Button