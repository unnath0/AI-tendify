import { useState, useEffect } from "react";
import { markAttendance, getStudents, updateAttendance } from "../services/api";

function Mark() {
  const [images, setImages] = useState([]);
  const [students, setStudents] = useState([]);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const data = await getStudents();
      setStudents(data);
    } catch (error) {
      console.error("Error fetching students:", error);
    }
  };

  const handleToggleAttendance = async (studentId, isPresent) => {
    try {
      await updateAttendance(studentId, isPresent);
      setStudents((prevStudents) =>
        prevStudents.map((student) =>
          student.student_id === studentId
            ? { ...student, is_present: !isPresent }
            : student,
        ),
      );
    } catch (error) {
      console.error("Failed to update attendance");
    }
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setImages((prev) => [...prev, ...files]);
  };

  const handleUpload = async () => {
    try {
      const response = await markAttendance(images);
      console.log("Upload Success: ", response);
      fetchStudents();
    } catch (error) {
      console.error("Upload Failed: ", error);
    }
  };

  return (
    <div className="p-5 content-center h-svh">
      <h1 className="text-center">
        Upload classroom photo(s) to mark attendance
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

      <h2 className="mt-5 text-center">Student List</h2>
      <table className="w-full mt-5 border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-200">
            <th className="border border-gray-300 px-4 py-2">Student ID</th>
            <th className="border border-gray-300 px-4 py-2">Name</th>
            <th className="border border-gray-300 px-4 py-2">Status</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr key={student.student_id} className="text-center">
              <td className="border border-gray-300 px-4 py-2">
                {student.student_id}
              </td>
              <td className="border border-gray-300 px-4 py-2">
                {student.name}
              </td>
              <td
                className="border border-gray-300 px-4 py-2 cursor-pointer"
                onClick={() =>
                  handleToggleAttendance(student.student_id, student.is_present)
                }
              >
                {student.is_present ? (
                  <span className="text-green-500 font-semibold">Present</span>
                ) : (
                  <span className="text-red-500 font-semibold">Absent</span>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Mark;
