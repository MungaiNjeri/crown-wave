
async function currentUser(token){
	await fetch('http://127.0.0.1:5555/current_user',{
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
		}})
	.then((res)=> {
		if(res.ok){
			return res
		}else{
			console.log(res)
		}
	})
//	.then (data => console.log(data))



}
/*
// Function to log in the user
async function login(username, password) {
    const loginEndpoint = "http://127.0.0.1:5555/login"; // Replace with your backend's login endpoint
    
    try {
        // Send a POST request to the login API
        const response = await fetch(loginEndpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        // Check if the login was successful
        if (response.ok) {
            const data = await response.json();
            
            // Extract the access token from the response
            const accessToken = data.access_token;
		currentUser(accessToken)
            
            
            
            console.log("Login successful:", data);
            
        } else {
            // Handle errors (e.g., invalid credentials)
            const errorData = await response.json();
            console.error("Login failed:", errorData);
            
        }
    } catch (error) {
        // Handle network or other unexpected errors
        console.error("Error during login:", error);
        
    }
}

// Example usage:
const username = "AhandsomeNigga"; // Replace with the user's username
const password = "12345678"; // Replace with the user's password
login(username, password);
*/

currentUser('eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTczNzEwNDY3NywianRpIjoiMjBhNWViZjktOTBiYi00Y2Q2LWE2YTgtNjJiZmNhOWQzNmRmIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNzM3MTA0Njc3LCJjc3JmIjoiOTMyNDUxMmYtY2Q3Ny00ODkxLWE1ZWEtMjA1NzRjM2ZlZmNjIiwiZXhwIjoxNzM3MTA1NTc3fQ.3rb9QhfIW8lWQk8cYFSYMNVl4mm4IP0ZuB3OzJAP52Q')
