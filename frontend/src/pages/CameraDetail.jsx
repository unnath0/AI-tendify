import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchEngagementAnalysis } from "../services/api";

function CameraDetail() {
  const { cameraId } = useParams();
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(true);
  const feedUrl = `http://127.0.0.1:8000/api/cameras/${cameraId}/`; // Direct live feed URL

  useEffect(() => {
    async function getAnalysisData() {
      try {
        const analysisResponse = await fetchEngagementAnalysis(cameraId);
        setAnalysis(analysisResponse);
      } catch (error) {
        console.error("Error fetching engagement analysis:", error);
      } finally {
        setLoading(false);
      }
    }
    getAnalysisData();
  }, [cameraId]);

  if (loading) {
    return <div className="text-center">Loading camera feed...</div>;
  }

  return (
    <div className="p-5">
      <h1 className="text-center text-xl font-bold">Camera {cameraId} Feed</h1>
      <div className="flex justify-center my-4">
        <img
          src={feedUrl} // Direct live feed URL
          alt={`Camera ${cameraId} Feed`}
          className="w-full max-w-3xl border"
        />
      </div>
      <div className="mt-5 p-4 border rounded">
        <h2 className="text-lg font-semibold">Engagement Analysis</h2>
        {analysis ? (
          <ul className="list-disc pl-5">
            <li>Attention Level: {analysis.attention_level}%</li>
            <li>Teacher Activity: {analysis.teacher_activity}</li>
            <li>Student Engagement: {analysis.student_engagement}</li>
          </ul>
        ) : (
          <p>No analysis data available</p>
        )}
      </div>
    </div>
  );
}

export default CameraDetail;
