
// Function to get the current user
async function getCurrentUser() {
    const API_URL = "http:127.0.0.1:5555/current_user"; 
    const token = localStorage.getItem("jwtToken");
  
    if (!token) {
      console.error("No token found. User might not be logged in.");
      return null; // Return null if the token is missing
    }
  
    try {
      // Make a GET request to the current user endpoint
      const response = await fetch(API_URL, {
        method: "GET",
        headers: {
          "Authorization": `Bearer ${token}`, // Include the token in the Authorization header
        },
      });
  
      // Check if the response is okay
      if (!response.ok) {
        if (response.status === 401) {
          console.error("Unauthorized. Token might be invalid or expired.");
        }
        throw new Error(`Failed to fetch user: ${response.status} - ${response.statusText}`);
      }
  
      // Parse the JSON response
      const user = await response.json();
      console.log("Current user fetched successfully:", user);
      return user; // Return the user object
    } catch (error) {
      console.error("Error fetching current user:", error.message);
      throw error; // Re-throw the error for further handling
    }
  }
  
  // Example usage
  getCurrentUser()
    .then((user) => {
      if (user) {
        console.log("Logged-in user:", user);
      } else {
        console.log("No user is logged in.");
      }
    })
    .catch((error) => {
      console.error("Failed to fetch user:", error.message);
    });
  