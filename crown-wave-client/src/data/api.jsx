
import axios from 'axios';

// API URL base
export const API_BASE_URL = 'http://127.0.0.1:5555'; 

//token


// Configure axios to include the token in all requests
export  const token = localStorage.getItem('jwtToken');




export const getUserProfile = async (userId) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/users/${userId}`,);
    return response;
  } catch (error) {
    console.error('Error fetching user profile:', error);
    throw error;
  }
};

export async function signUp(userData){
  

  fetch(`${API_BASE_URL}/signup`, {
      method: 'POST',
      body: JSON.stringify(userData),
      headers: {
        'Content-type': 'application/json;',
      }
      })
      .then(function(response){ 
          return response.json()})
      .then(function(data)
          {return 1;})
      .catch(error => console.error('Error:', error)); 
   


}

export const loginUser = async (credentials) => {
  try {
    const response = await fetch(`${API_BASE_URL}/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(credentials),
    });

    // Check if the response is okay
    if (!response.ok) {
      throw new Error(`Login failed: ${response.status} - ${response.statusText}`);
    }

    // Parse the JSON response
    const data = await response.json();

    // Assuming the API returns a JWT token under the key "token"
    if (data.access_token) {
      // Save the token in localStorage
      localStorage.setItem("jwtToken", data.access_token);
      console.log("Login successful. Token stored in localStorage.");
    } else {
      console.error("Token not found in response.");
    }

    return data; // Return the API response
  } catch (error) {
    console.error("Error during login:", error);
    throw error; // Re-throw the error for further handling
  }
};

