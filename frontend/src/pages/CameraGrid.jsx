import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const CameraGrid = () => {
  const [cameras, setCameras] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/cameras/")
      .then((res) => res.json())
      .then((data) => setCameras(data))
      .catch((err) => console.error("Error fetching cameras:", err));
  }, []);

  return (
    <div className="grid grid-cols-3 gap-4 p-5">
      {cameras.map((camera) => (
        <div
          key={camera.camera_id}
          className="border rounded-lg p-2 cursor-pointer shadow-lg hover:shadow-xl"
          onClick={() => navigate(`/cameras/${camera.camera_id}`)}
        >
          <img
            src={`http://127.0.0.1:8000/api/cameras/${camera.camera_id}/`} // Live feed
            alt={camera.location}
            className="w-full h-40 object-cover rounded"
          />
          <p className="text-center font-semibold mt-2">{camera.location}</p>
        </div>
      ))}
    </div>
  );
};

export default CameraGrid;
