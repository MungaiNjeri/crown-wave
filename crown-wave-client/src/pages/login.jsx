import React from "react";
import './pages-styles/login.css'
import Input from "../components/input";
import Button from "../components/button";
function Login(){

    return(
    <>
            <div id="login">
                <div id="login-left-aside">

                </div>
                <div id="login-right-aside">
                    <h1 id="login-h1">Crown wave</h1>
                    <h2>Log in to your account</h2>
                    <form action="">

                    <p>Username</p>
                    <Input
                        label="Username"
                        type="text"
                        placeholder="Enter your username"
                        className = "input"
                    />

                    <p>Enter password</p>
                    <Input
                        label="Password"
                        type="password"
                        placeholder="Enter your password"
                        className = "input"
                    />

                    </form>
                    <Button 
                            type="submit"
                            placeholder="Log in"
                            //onClick: PropTypes.func.isRequired,
                            className = 'button'
                    />

                </div>
            </div>
    </>
    )

}

export default Login