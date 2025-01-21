import React from "react";
import PropTypes from "prop-types";
import './comp-styles/form.css'
function Form(
    {
        type = "text",
        action = "", 
        className = "",
        ...rest
      }
){
    return(
        <>
            <form action="" className={`input-wrapper ${className}`}>


            </form>
        </>
    )
}
export default Form