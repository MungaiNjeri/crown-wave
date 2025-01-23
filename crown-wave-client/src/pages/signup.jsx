import React, { useState } from "react";

import Input from "../components/input";
import Button from "../components/button";
import './pages-styles/signup.css'
import { signUp } from "../data/api";

function Signup(){

    const [errors, setErrors] = useState({});
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')
   
    const validate = () => {
        const errors = {};
        if (name === '') errors.username = 'Username is required';
        if (email === '') {
          errors.email = 'Email is required';
        } else if (!/\S+@\S+\.\S+/.test(email)) {
          errors.email = 'Email address is invalid';
        }
        if (password === '') {
          errors.password = 'Password is required';
        } else if (password.length < 6) {
          errors.password = 'Password must be at least 6 characters';
        }
        if (password !== confirmPassword) {
          errors.confirmPassword = 'Passwords do not match';
        }
        return errors;
      };
    
 
  
    function handleSubmit(e){
      e.preventDefault()
      const validationErrors = validate();
      if (Object.keys(validationErrors).length > 0) {
          setErrors(validationErrors);
          return;
      }
      signUp({
        username:name,
        email:email,
        password:password,
      })

      setName('')
      setEmail('')
      setPassword('')
      setConfirmPassword('')
      console.log('submited')
        
    }

    return(
        <>
            <div id="signup">
                <div id="signup-left-aside">

                </div>
                <div id="signup-right-aside">
                    <h1 id="signup-h1">Crown wave</h1>
                    <h2 id="signup-h2">Join the movement</h2>
                    <form onSubmit={handleSubmit}>

                    <p>Username</p>
                    <Input
                        label="Username"
                        value={name  }
                        type="text"
                        placeholder="Enter your username"
                        className = "input"
                        onChange={(e)=>{setName(e.target.value)}}
                    />
                   {errors.username && <span className="error">{errors.username}</span>}
                    <p>Email</p>
                    <Input
                        label="Email"
                        type="email"
                        value={email }
                        placeholder="Enter your email"
                        className = "input"
                        onChange={(e)=>{setEmail(e.target.value)}}
                    />
                      {errors.email && <span className="error">{errors.email}</span>}
                    <p>Enter password</p>
                    <Input
                        label="Password"
                        type="password"
                        placeholder="Enter your password"
                        className = "input"
                        value={password  }
                        onChange={(e)=>{setPassword(e.target.value)}}
                    />
                      {errors.password && <span className="error">{errors.password}</span>}
                    <p>Confirm Password</p>
                    <Input
                        label="Password"
                        type="password"
                        placeholder="confirm your password"
                        value={confirmPassword }
                        className = "input"
                        onChange={(e)=>{setConfirmPassword(e.target.value)}}
                    />
                    {errors.confirmPassword && (
                    <span className="error">{errors.confirmPassword}</span>
                    )}
                    <br/>
                    <Button 
                            type="submit"
                            placeholder="Signup"
                            className = 'button'
                    />
                    </form>

                    <p>Already have an account? <a href="/login">Log in.</a></p>
                </div>
            </div>
        
        </>
    )
}

export default Signup