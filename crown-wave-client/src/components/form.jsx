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
            <form action={action} className={` ${className}`}>
            </form>
        </>
    )
}


Form.propTypes = {
 
  type: PropTypes.string,
  action: PropTypes.string,
  className: PropTypes.string,
};
export default Form