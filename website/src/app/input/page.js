// app/input/page.js
"use client";

import { useState } from 'react';

export default function InputForm() {
  const [npk, setNpk] = useState({ n: '', p: '', k: '' });
  const [soilMoisture, setSoilMoisture] = useState('');
  const [crop, setCrop] = useState('');
  const [feasibility, setFeasibility] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const response = await fetch('/api/calculate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ npk, soilMoisture, crop }),
    });
    const data = await response.json();
    setFeasibility(data.feasibility);
  };

  return (
    <div>
      <div className="container d-flex align-items-center justify-content-center" style={{ height: '80vh' }}>
        <div className="w-50">
          <h1 className="text-center mb-4">Farming Feasibility Calculator</h1>
          <form onSubmit={handleSubmit}>
            <div className="mb-3">
              <label className="form-label">Nitrogen (N):</label>
              <input type="number" className="form-control" value={npk.n} onChange={(e) => setNpk({ ...npk, n: e.target.value })} />
            </div>
            <div className="mb-3">
              <label className="form-label">Phosphorus (P):</label>
              <input type="number" className="form-control" value={npk.p} onChange={(e) => setNpk({ ...npk, p: e.target.value })} />
            </div>
            <div className="mb-3">
              <label className="form-label">Potassium (K):</label>
              <input type="number" className="form-control" value={npk.k} onChange={(e) => setNpk({ ...npk, k: e.target.value })} />
            </div>
            <div className="mb-3">
              <label className="form-label">Soil Moisture:</label>
              <input type="number" className="form-control" value={soilMoisture} onChange={(e) => setSoilMoisture(e.target.value)} />
            </div>
            <div className="mb-3">
              <label className="form-label">Crop Type:</label>
              <input type="text" className="form-control" value={crop} onChange={(e) => setCrop(e.target.value)} />
            </div>
            <button type="submit" className="btn btn-primary w-100">Calculate Feasibility</button>
          </form>
          {feasibility !== null && <p className="mt-3 text-center">Feasibility: {feasibility}%</p>}
        </div>
      </div>
    </div>
  );
}
