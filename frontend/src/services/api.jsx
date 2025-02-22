import axios from "axios";

const API_URL = "http://localhost:8000/api"; // Change this based on your backend

export const markAttendance = async (images) => {
  const formData = new FormData();
  images.forEach((image) => {
    formData.append("images", image); // Ensure all images go under the "images" key
  });

  try {
    const response = await axios.post(
      `${API_URL}/students/recognize/`,
      formData,
      {
        headers: { "Content-Type": "multipart/form-data" },
      },
    );
    return response.data;
  } catch (error) {
    console.error("Upload failed:", error);
    throw error;
  }
};

export const trainModel = async (images) => {
  const formData = new FormData();
  images.forEach((image) => {
    formData.append("images", image); // Ensure all images go under the "images" key
  });

  try {
    const response = await axios.post(`${API_URL}/students/encode/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    return response.data;
  } catch (error) {
    console.error("Upload failed:", error);
    throw error;
  }
};

export const getStudents = async () => {
  try {
    const response = await axios.get(`${API_URL}/students/retrieve_all/`);
    return response.data;
  } catch (error) {
    console.error("Failed to fetch students:", error);
    throw error;
  }
};

export const updateAttendance = async (studentId, isPresent) => {
  try {
    const response = await axios.patch(
      `${API_URL}/students/update/${studentId}/`, // Use the correct API endpoint
      { is_present: !isPresent }, // Toggle presence
      {
        headers: { "Content-Type": "application/json" },
      },
    );
    return response.data;
  } catch (error) {
    console.error("Failed to update attendance:", error);
    throw error;
  }
};
