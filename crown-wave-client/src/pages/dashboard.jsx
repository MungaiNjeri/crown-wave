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

                </div>


            </div>
        </>
    )
}

export default Dashboard