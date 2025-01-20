import React from "react";
import PropTypes from "prop-types";
import './comp-styles/input.css'

const Input = ({
  type = "text",
  placeholder = "",
  value,
  onChange,
  error,
  className = "",
  ...rest
}) => {
  return (
    <div className={`input-wrapper ${className}`}>
      <input
        type={type}
        placeholder={placeholder}
        //value={value}
        //onChange={onChange}
        className={`input ${error ? "input-error" : ""}`}
        {...rest}
      />
      {error && <small className="error-message">{error}</small>}
    </div>
  );
};

Input.propTypes = {
 
  type: PropTypes.string,
  placeholder: PropTypes.string,
  //value: PropTypes.string.isRequired,
  //onChange: PropTypes.func.isRequired,
  error: PropTypes.string,
  className: PropTypes.string,
};

export default Input;
