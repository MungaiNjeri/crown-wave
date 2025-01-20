import React, { useState } from 'react' 
import { BrowserRouter as Router,Routes,Route } from 'react-router-dom'

import Signup from './pages/signup'
import Login from './pages/login'
import Dashboard from './pages/dashboard'

import './App.css'

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


      </Routes>
    </Router>  
    </>
  )
}

export default App
