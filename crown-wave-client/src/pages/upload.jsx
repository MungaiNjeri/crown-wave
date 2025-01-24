import React, { useState } from "react";
import Button from "../components/button";
import './pages-styles/upload.css'

const ImageUploader = ({ onImageUpload }) => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setImage(file);

      // Create a preview URL for the image
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    if (image) {
      onImageUpload(image); // Pass the uploaded image to the parent component
      alert("Image uploaded successfully!");
    } else {
      alert("Please select an image to upload.");
    }
  };

  return (
    <>
      <div id="upload">
        <h1>Upload files</h1>
        <h3>add your screenshot here.</h3>
         <div id="upload-preview">

         </div>
         <div><h2>file name:</h2>
              <p>screenshot.jpeg</p> 
         </div>
         <Button 
          type="submit"
          placeholder="upload"
          
         />
         
      </div>


    
    </>
  
  );
};

export default ImageUploader;
