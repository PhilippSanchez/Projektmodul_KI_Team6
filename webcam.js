import React, { useRef } from 'react';
import axios from 'axios';

function WebcamCapture() {
  const webcamRef = useRef(null);
  
  const capture = async () => {
    const imageSrc = webcamRef.current.getScreenshot();
    try {
      const response = await axios.post('http://localhost:5000/analyze', {
        image: imageSrc
      });
      
      const { emotion, score, bbox } = response.data;
      console.log(emotion, score, bbox); // Do something with the data
    } catch (error) {
      console.error("Error processing the image", error);
    }
  };

  return (
    <>
      {/* Setup Webcam */}
      {/* Add a button that calls capture when clicked */}
    </>
  );
}

export default WebcamCapture;