import React, { useState } from "react";
import './pages-styles/login.css'
import Input from "../components/input";
import Button from "../components/button";
import { loginUser } from "../data/api";
function Login(){
    const [username,setUserName] = useState('')
    const [password, setPassword] = useState("")

    function handleSubmit(e){
        e.preventDefault()
        loginUser({
            username:username,
            password:password})
            
        console.log('submit')
        
    }


    return(
    <>
            <div id="login">
                <div id="login-left-aside">

                </div>
                <div id="login-right-aside">
                    <h1 id="login-h1">Crown wave</h1>
                    <h2>Log in to your account</h2>
                    <form onSubmit={handleSubmit}>

                    <p>Username</p>
                    <Input
                        label="Username"
                        type="text"
                        value={username}
                        onChange={(e)=>{setUserName(e.target.value)}}
                        placeholder="Enter your username"
                        className = "input"
                    />

                    <p>Enter password</p>
                    <Input
                        label="Password"
                        type="password"
                        value={password}
                        onChange={(e)=>{setPassword(e.target.value)}}
                        placeholder="Enter your password"
                        className = "input"
                    />
                    <br />
                    <Button 
                            type="submit"
                            placeholder="Log in"
                            //onClick: PropTypes.func.isRequired,
                            className = 'button'
                    />


                    </form>

                </div>
            </div>
    </>
    )

}

export default Login