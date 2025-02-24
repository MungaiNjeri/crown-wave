import React, { useState } from "react";
import axios from "axios";

const packages = [
  { name: "Elite Package", price: 1000 },
  { name: "Prestige Membership", price: 2000 },
  { name: "Delux Membership", price: 3500 },
  { name: "Grand Membership", price: 5500 },
];

const ServicePackages = () => {
  const [phone, setPhone] = useState("");

  const handlePayment = async (amount) => {
    if (!phone) {
      alert("Please enter your M-Pesa phone number");
      return;
    }

    try {
      const response = await axios.post("http://localhost:5000/stkpush", {
        phone,
        amount,
      });
      alert("Payment request sent. Check your phone!");
    } catch (error) {
      console.error("Payment error:", error);
      alert("Payment failed!");
    }
  };

  return (
    <div className="p-5">
      <h2 className="text-xl font-bold mb-4">Service Package</h2>
      <input
        type="text"
        placeholder="Enter M-Pesa number"
        value={phone}
        onChange={(e) => setPhone(e.target.value)}
        className="border p-2 rounded-md mb-4 block w-full"
      />
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {packages.map((pkg, index) => (
          <div key={index} className="bg-purple-700 text-white p-6 rounded-lg shadow-lg">
            <h3 className="text-lg font-bold">{pkg.name}</h3>
            <button
              className="mt-4 bg-white text-purple-700 px-4 py-2 rounded-md"
              onClick={() => handlePayment(pkg.price)}
            >
              Pay {pkg.price} KES
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ServicePackages;
