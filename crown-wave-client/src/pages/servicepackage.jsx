import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [selectedPackage, setSelectedPackage] = useState(null);
  const [phoneNumber, setPhoneNumber] = useState('');
  const [paymentStatus, setPaymentStatus] = useState(null);

  const handlePackageSelection = (packageName) => {
    setSelectedPackage(packageName);
  };

  const handlePhoneNumberChange = (event) => {
    setPhoneNumber(event.target.value);
  };

  const handlePayment = async () => {
    try {
      // Replace with your actual M-Pesa API credentials and endpoints
      const apiUrl = 'https://your-mpesa-api-endpoint/stkpush';
      const apiKey = 'YOUR_API_KEY';
      const apiSecret = 'YOUR_API_SECRET';
      const auth = Basic `${Buffer.from(`${apiKey}:${apiSecret}`).toString('base64')}`;

      const headers = {
        Authorization: auth,
        'Content-Type': 'application/json',
      };

      const body = {
        // M-Pesa API request parameters based on the selected package
        // Example:
        Amount: selectedPackage === 'Elite' ? 1000 : 
               selectedPackage === 'Prestige' ? 2000 : 
               selectedPackage === 'Deluxe' ? 3500 : 
               selectedPackage === 'Grand' ? 5500 : 0,
        PhoneNumber: phoneNumber,
        // Other required parameters (e.g., BusinessShortCode, Passkey)
      };

      const response = await axios.post(apiUrl, body, { headers });

      if (response.status === 200) {
        setPaymentStatus('Payment initiated successfully.');
        // Handle successful payment initiation (e.g., display a confirmation message)
      } else {
        setPaymentStatus('Payment initiation failed.');
        // Handle payment initiation error (e.g., display an error message)
      }
    } catch (error) {
      console.error('Error during payment initiation:', error);
      setPaymentStatus('An error occurred during payment.');
    }
  };

  return (
    <div className="container">
      <h1>Service Packages</h1>

      <div className="packages">
        {/* ... (package cards as before) ... */}
      </div>

      {selectedPackage && (
        <div className="selected-package">
          <h2>Selected Package: {selectedPackage}</h2>
          <p>Enter your phone number:</p>
          <input type="tel" value={phoneNumber} onChange={handlePhoneNumberChange} />
          <button onClick={handlePayment}>Pay with M-Pesa</button>
          <p>{paymentStatus}</p>
        </div>
      )}
    </div>
  );
}

export default App;