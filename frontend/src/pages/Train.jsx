import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { trainModel } from "../services/api";

function TrainModel() {
  const navigate = useNavigate();

  const [images, setImages] = useState([]);
  const [result, setResult] = useState();

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setImages((prev) => [...prev, ...files]);
  };

  const handleUpload = async () => {
    try {
      const response = await trainModel(images);
      console.log("Upload Success: ", response);
      setResult(response.message);
      navigate("/");
    } catch (error) {
      console.error("Upload Failed: ", error);
    }
  };

  return (
    <div className="p-5 content-center h-svh">
      <h1 className="text-center">
        Upload individual student photos to train model
      </h1>
      <div className="flex justify-center gap-2">
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleFileChange}
          className="px-4 py-2 border rounded-sm cursor-pointer"
        />
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded-sm cursor-pointer"
          onClick={handleUpload}
        >
          Upload Images
        </button>
      </div>

      <p className="text-center">{result}</p>
    </div>
  );
}

export default TrainModel;
