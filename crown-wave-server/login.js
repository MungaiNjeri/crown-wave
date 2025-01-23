// Function to handle user login
async function loginUser(credentials) {
    const API_URL = "http:127.0.0.1:5555/login"; 
    try {
      const response = await fetch(API_URL, {
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
  }
  
  // Example usage
  const credentials = {
    username: "ninja", // Replace with user input
    password: "1234567", // Replace with user input
  };
  
  loginUser(credentials)
    .then((data) => {
      console.log("Logged in successfully:", data);
    })
    .catch((error) => {
      console.error("Login failed:", error.message);
    });
  