import React, { useEffect, useState } from "react";
import axios from "axios";
import { parsePath } from "react-router-dom";

const UserProfile = () => {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const username = "";
  

  // Fetch the CEO profile from the API
  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await axios.get("http://127.0.0.1:5555/current_user", {
          headers: {
            'username': 'your-username',
          },
        });
        setProfile(response.data);
      } catch (err) {
        setError("Failed to fetch user profile. Please try again later.");
        console.error("Error fetching profile:", err);
      } finally {
        setLoading(false);
      }
    };
  
    fetchProfile();
  }, []);
  
  
    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;
  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <img
          src={profile.image || "data:image/jpeg;base64,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"}
          alt="Profile"
          style={styles.image}
        />
        <h1 style={styles.name}>{profile.name || "CEO "}</h1>
        <p style={styles.status}>{profile.title || "Active"}</p>
        <p style={styles.bio}>{profile.bio || "queen diva"}</p>
        <p style={styles.package}>
          <strong>Package:</strong> {profile.package || "No package assigned"}
        </p>
        <div style={styles.contact}>
          <a href={`mailto:${profile.email}`} style={styles.link}>
            Email
          </a>
          <a href={profile.linkedin} target="_blank" rel="noopener noreferrer" style={styles.link}>
            LinkedIn
          </a>
        </div>
      </div>
    </div>
  );
};

const styles = {
  container: {
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    height: "100vh",
    width:"100%",
    backgroundImage: "linear-gradient(to right, blue, red)",
    margin:0,
    padding:0
  },
  card: {
    width: "400px",
    padding: "20px",
    borderRadius: "10px",
    boxShadow: "0 4px 8px rgba(0,0,0,0.1)",
    backgroundColor: "#fff",
    textAlign: "center",
  },
  image: {
    width: "100px",
    height: "100px",
    borderRadius: "50%",
    marginBottom: "10px",
  },
  name: {
    fontSize: "24px",
    fontWeight: "bold",
  },
  title: {
    fontSize: "18px",
    color: "#666",
  },
  bio: {
    fontSize: "16px",
    margin: "10px 0",
  },
  package: {
    fontSize: "16px",
    margin: "10px 0",
    color: "#333",
  },
  contact: {
    marginTop: "15px",
  },
  link: {
    margin: "0 10px",
    color: "#007bff",
    textDecoration: "none",
    fontSize: "14px",
  },
};

export default UserProfile;
