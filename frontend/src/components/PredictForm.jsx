import React, { useState } from 'react';

function PredictForm() {
  const [formData, setFormData] = useState({
    age: '',
    systolic_bp: '',
    diastolic_bp: '',
    gender: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ features: {
          age: Number(formData.age),
          systolic_bp: Number(formData.systolic_bp),
          diastolic_bp: Number(formData.diastolic_bp),
          gender: Number(formData.gender)
        }})
      });
      if (!response.ok) {
        throw new Error(`Server error ${response.status}`);
      }
      const data = await response.json();
      setResult(data.probabilities);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '400px', margin: 'auto' }}>
      <h2>CardioVision Prediction</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Age:</label><br />
          <input type="number" name="age" value={formData.age} onChange={handleChange} required />
        </div>
        <div>
          <label>Systolic BP:</label><br />
          <input type="number" name="systolic_bp" value={formData.systolic_bp} onChange={handleChange} required />
        </div>
        <div>
          <label>Diastolic BP:</label><br />
          <input type="number" name="diastolic_bp" value={formData.diastolic_bp} onChange={handleChange} required />
        </div>
        <div>
          <label>Gender (0=Female, 1=Male):</label><br />
          <input type="number" name="gender" min="0" max="1" value={formData.gender} onChange={handleChange} required />
        </div>
        <button type="submit" disabled={loading} style={{ marginTop: '10px' }}>
          {loading ? 'Predicting...' : 'Predict'}
        </button>
      </form>
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {result && (
        <div style={{ marginTop: '20px' }}>
          <h3>Predicted Probabilities</h3>
          <ul>
            {Object.entries(result).map(([key, val]) => (
              <li key={key}>{key}: {(val * 100).toFixed(2)} %</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default PredictForm;
