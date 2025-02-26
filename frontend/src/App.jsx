import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Mark from "./pages/Mark";
import Train from "./pages/Train";
import CameraGrid from "./pages/CameraGrid";
import CameraDetail from "./pages/CameraDetail";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Mark />} />
        <Route path="/train" element={<Train />} />
        <Route path="/cameras" element={<CameraGrid />} />
        <Route path="/cameras/:cameraId" element={<CameraDetail />} />
      </Routes>
    </Router>
  );
}

export default App;
