import React, { useState } from 'react' 
import { BrowserRouter as Router,Routes,Route } from 'react-router-dom'

import Signup from './pages/signup'
import Login from './pages/login'
import Dashboard from './pages/dashboard'

import './App.css'
import Deposit from './pages/deposit'
import Withdraw from './pages/withdraw'
import Transfer from './pages/transfer'
import Product from './pages/product'
import ImageUploader from './pages/upload'

function App() {
  const [count, setCount] = useState(0)

  return (

    <>
    <Router>
      <Routes>
        {/*<Route path="/" element={} />*/}
        <Route path='/signup' element = {<Signup />}></Route>
        <Route path='/login' element = {<Login />}></Route>
        <Route path='/' element = {<Dashboard />}></Route>
        <Route path='/deposit' element = {<Deposit />}></Route>
        <Route path='/withdraw' element = {<Withdraw />}></Route>
        <Route path='/transfer' element = {<Transfer />}></Route>
        <Route path ='/product' element={<Product />}></Route>
        <Route path ='/upload' element={<ImageUploader />}></Route>
        


      </Routes>
    </Router>  
    </>
  )
}

export default App
