import React from "react";
import Button from "../components/button";
import './pages-styles/product.css'


const Product = ({ imageUrl, imageName }) => {
  const handleDownload = () => {
    // Create an invisible anchor element
    const anchor = document.createElement("a");
    anchor.href = imageUrl; // Set the URL
    anchor.download = imageName || "downloaded-image"; // Set the download file name
    document.body.appendChild(anchor); // Append anchor to the body
    anchor.click(); // Trigger the download
    document.body.removeChild(anchor); // Remove the anchor element
  };

  return (
    <div className="Product-downloader">
      <img
        src={'https://images.pexels.com/photos/7676408/pexels-photo-7676408.jpeg?auto=compress&cs=tinysrgb&w=600'}
        alt="Preview"
      />
      <br />
        <Button 
          type="submit"
          placeholder="Download"
          //onClick: PropTypes.func.isRequired,
          className = 'button'
          />

    </div>
  );
};

export default Product;
