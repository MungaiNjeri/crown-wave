import React from "react";
import Input from "../components/input";
import './pages-styles/signup.css'

function Signup(){
    return(
        <>
            <div id="signup">
                <div id="signup-left-aside">

                </div>
                <div id="signup-right-aside">
                    <h1 id="signup-h1">Crown wave</h1>
                    <h2 id="signup-h2">Join the movement</h2>
                    <form action="">

                    <p>Username</p>
                    <Input
                        label="Username"
                        type="text"
                        placeholder="Enter your username"
                        className = "input"
                    />
                    <p>Email</p>
                    <Input
                        label="Email"
                        type="email"
                        placeholder="Enter your email"
                        className = "input"
                    />
                    <p>Enter password</p>
                    <Input
                        label="Password"
                        type="password"
                        placeholder="Enter your password"
                        className = "input"
                    />
                    <p>Confirm Password</p>
                    <Input
                        label="Password"
                        type="password"
                        placeholder="confirm your password"
                        className = "input"
                    />
                    </form>

                    <p>Already have an account? <a href="/login">Log in.</a></p>
                </div>
            </div>
        
        </>
    )
}

export default Signup