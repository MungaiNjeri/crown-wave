import React, { useState } from "react";
import Button from "../components/button";


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
    <div style={{ textAlign: "center", margin: "20px" }}>
      <form onSubmit={handleSubmit}>
        <input
          type="file"
          accept="image/*"
          onChange={handleFileChange}
          
        />
        {preview && (
          <div style={{ marginBottom: "10px" }}>
            <img
              src={preview}
              alt="Preview"
              
            />
          </div>
        )}
        <Button 
          type="submit"
          placeholder="Upload"
          //onClick: PropTypes.func.isRequired,
          className = 'button'
          />
      </form>
    </div>
  );
};

export default ImageUploader;
