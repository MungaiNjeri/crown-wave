import { func } from "prop-types";
import Input from "../components/input";
import Button from "../components/button";
import React from "react";
import './pages-styles/deposit.css'

function Deposit(){
    return(
        <>
        <div id = "deposit">
            <form >
                <div id="deposit-wrapper">
                    <h2>Deposit</h2>                
                    <Input
                        label="amount"
                        type="text"
                        placeholder="Enter amount" 
                        className = "input"
                    />
                </div>
                    <Button 
                        type="submit"
                        placeholder="Deposit"
                        //onClick: PropTypes.func.isRequired,
                        className = 'button'
                    />

            </form>

        </div>

        </>
    )
}

export default Deposit