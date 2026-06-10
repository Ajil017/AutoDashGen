import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Ensure you have the CSS file we created

function App() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);

  // Helper function to handle file downloads from the browser
  const download = (content, fileName) => {
    const element = document.createElement("a");
    const fileBlob = new Blob([content], { type: 'text/plain' });
    element.href = URL.createObjectURL(fileBlob);
    element.download = fileName;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first!");
    
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Connecting to the Al Processing Engine on the Backend
      const res = await axios.post('http://127.0.0.1:5000/upload', formData);
      setResults(res.data);
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Backend not responding. Ensure python app.py is running.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>AutoDashGen Dashboard Output</h1>
      </header>

      <div className="upload-section card">
        <h3>User Interaction: Data Upload</h3>
        <input type="file" onChange={(e) => setFile(e.target.files[0])} accept=".csv" />
        <button className="btn-primary" onClick={handleUpload} disabled={loading}>
          {loading ? "Analyzing Data..." : "Analyze & Generate"}
        </button>
      </div>
      
      // ... Inside your return statement ...
{results && (
  <div className="pbi-workspace">
    {/* 1. Ribbon Controls [cite: 70] */}
    <div className="ribbon">
      <button onClick={() => window.print()}>Print Report</button>
      <button onClick={() => alert("Publishing to Workspace...")}>Publish</button>
    </div>

    <div className="main-content" style={{ display: 'flex' }}>
      {/* 2. Filter & Fields Sidebar [cite: 66] */}
      <div className="pbi-sidebar">
        <h4>Fields</h4>
        {results.profile.map(p => <div className="field-item">✓ {p.column}</div>)}
      </div>

      {/* 3. Hero Visual & Insight Area [cite: 65] */}
      <div className="dashboard-canvas">
        <div className="hero-visual card">
          <h3>{results.recommendations[0].chart} Recommendation</h3>
          <p className="insight-text">"{results.recommendations[0].insight}"</p>
          {/* Chart Rendering logic here */}
        </div>

        {/* 4. Export Controls [cite: 71, 72] */}
        <div className="export-footer">
          <button className="btn-export" onClick={() => download(results.artifacts.dax.join('\n'), 'AutoDash.dax')}>
             Export Dashboard (.dax)
          </button>
        </div>
      </div>
    </div>
  </div>
)}
    </div>
  );
}

export default App;