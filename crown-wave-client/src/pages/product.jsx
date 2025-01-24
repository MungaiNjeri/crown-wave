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
    <div id="product-wrapper">
          <div id="product-details">
              <h1>Poang</h1>
              <h3>Rocking chair</h3>
              <p>Lorem ipsum dolor sit amet, consectetur adipisicing elit. Omnis sapiente aliquid quibusdam. Provident veniam deleniti, facere asperiores qui sapiente ea.</p>
              <Button 
                        type="submit"
                        placeholder="download" />
            </div>
            <div id="product-image-wrapper">
              <h1><i class="bi bi-currency-exchange"></i>299</h1>
              <div id="product-image">

              </div>

            </div>

    </div>
 
  );
};

export default Product;
