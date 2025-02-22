import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import Mark from "./pages/Mark";
import Train from "./pages/Train";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Mark />} />
        <Route path="/train" element={<Train />} />
      </Routes>
    </Router>
  );
}

export default App;
