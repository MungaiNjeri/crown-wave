import React from "react";
import  './pages-styles/dashboard.css'


function Dashboard(){
    return(
        <>
            <div id='dashboard'>
                <div id='dashboard-menu'>
                    <div className="dashboard-nav">
                        <h3  className="nav-item"> <i class="bi bi-activity"></i>Statistics</h3>
                    </div>
                    <div  className="dashboard-nav">
                        <h3  className="nav-item"><i class="bi bi-plugin"></i>Recharge</h3>
                    </div>
                    <div  className="dashboard-nav">
                        <h3  className="nav-item"><i class="bi bi-basket3-fill"></i>Product</h3>
                    </div>
                    <div  className="dashboard-nav">
                        <h3  className="nav-item"><i class="bi bi-arrow-bar-right"></i>Transfer</h3>
                    </div>
                    <div  className="dashboard-nav">
                        <h3  className="nav-item"><i class="bi bi-cash-stack"></i>Withdraw</h3>
                    </div>
                    <div  className="dashboard-nav">
                        <h3 className="nav-item"><i class="bi bi-bell-fill"></i>Notifications</h3>
                    </div>
                </div>

                <div id= 'dashboard-main'>
                    <div id="main-header">
                        <div> <h1>Dashboard</h1></div>
                        <div id="main-user">
                            <div id="main-date">
                                <i class="bi bi-calendar"></i>
                                <h3> January 21</h3>
                            </div>
                            <div id="main-user-icon">
                                <img src="https://images.pexels.com/photos/35537/child-children-girl-happy.jpg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1" alt="" width={50} height={50} />
                            </div>
                        </div>
                    </div>

                    <div id="dashboard-main-main">
                        <div id="main-main-summary">
                            <div id="main-main-status">

                            </div>

                            <div id="main-main-account">
                                <h2>Balance</h2>
                                <h1><i className="bi bi-currency-exchange"></i>100,000</h1>
                                <h3><i className="bi bi-graph-up-arrow"></i> +35%</h3>
                            </div>
                        </div>
                        
                        <div id="main-main-ads">
                                <p>Ads</p>
                        </div>

                    </div>
                    <div id="dashboard-transaction">
                        <table className="transaction-Table">
                                <tr className="transaction-Row">
                                    <th>No.</th>
                                    <th>description</th>
                                    <th>20,000</th>
                                    <th>12th Jan</th>
                                    
                                </tr>
                                <tr className="transaction-Row">
                                    <td>1</td>
                                    <td>withdraw</td>
                                    <td>32,323</td>
                                    <td>6th Jan</td>
                                </tr>
                                <tr className="transaction-Row">
                                    <td>2</td>
                                    <td>deposit</td>
                                    <td>123,423</td>
                                    <td>6th Jan</td>
                                </tr>
                                <tr className="transaction-Row">
                                    <td>3</td>
                                    <td>transfer</td>
                                    <td>45,677</td>
                                    <td>2nd Jan</td>
                                </tr>
                                <tr className="transaction-Row">
                                    <td>4</td>
                                    <td>deposit</td>
                                    <td>234,8934</td>
                                    <td>1st Jan</td>
                                </tr>
                        </table>

                    </div>

                </div>


            </div>
        </>
    )
}

export default Dashboard