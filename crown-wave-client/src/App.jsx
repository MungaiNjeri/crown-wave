import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Signup from "./pages/signup";
import Login from "./pages/login";
import Dashboard from "./pages/dashboard";
import Deposit from "./pages/deposit";
import Withdraw from "./pages/withdraw";
import Transfer from "./pages/transfer";
import UserProfile from "./pages/userprofile";
import Product from "./pages/product";
import ImageUploader from "./pages/upload";

import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <Router>
      <Routes>
        {/* Define your routes */}
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />
        <Route path="/" element={<Dashboard />} />
        <Route path="/deposit" element={<Deposit />} />
        <Route path="/withdraw" element={<Withdraw />} />
        <Route path="/transfer" element={<Transfer />} />
        <Route path="/userprofile" element={<UserProfile />} />
        <Route path="/product" element={<Product />} />
        <Route path="/upload" element={<ImageUploader />} />
      </Routes>
    </Router>
  );
}

export default App;
