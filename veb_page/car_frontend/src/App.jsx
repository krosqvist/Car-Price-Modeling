import { useState } from 'react'
import './App.css'

function App() {
  const [form, setForm] = useState({
    Maker: '',
    Genmodel: '',
    Gearbox: '',
    Fuel_type: '',
    Bodytype: '',
    Engin_size: 1.6,
    Reg_year: 2018,
    Runned_Miles: 100000,
  })

  const [result, setResult] = useState(null)
  const [image, setImage] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    const response = await fetch('/run', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form),
    });
    console.log(form)
    const data = await response.json()
    setResult(data.result)
    setImage(data.image)
    setLoading(false)
  };

  return (
    <div className="app-container">
      <div className="form-card">
        <h2>Car Price Estimator</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Maker
            <input name="Maker" value={form.Maker} onChange={handleChange} required />
          </label>

          <label>
            Model
            <input name="Genmodel" value={form.Genmodel} onChange={handleChange} required />
          </label>

          <label>
            Gearbox
            <select name="Gearbox" value={form.Gearbox} onChange={handleChange} required>
              <option value="">Select Gearbox</option>
              <option>Automatic</option>
              <option>Semi-Automatic</option>
              <option>Manual</option>
            </select>
          </label>

          <label>
            Fuel Type
            <select name="Fuel_type" value={form.Fuel_type} onChange={handleChange} required>
              <option value="">Select Fuel Type</option>
              <option>Diesel</option>
              <option>Petrol</option>
              <option>Hybrid</option>
              <option>Electric</option>
            </select>
          </label>

          <label>
            Bodytype
            <select name="Bodytype" value={form.Bodytype} onChange={handleChange} required>
              <option value="">Select Bodytype</option>
              <option>Coupe</option>
              <option>Convertible</option>
              <option>Saloon</option>
              <option>MPV</option>
              <option>Hatchback</option>
              <option>Estate</option>
              <option>Pickup</option>
              <option>SUV</option>
              <option>Van</option>
            </select>
          </label>

          <div className="slider-group">
            <label>Engine Size: {form.Engin_size} L</label>
            <input type="range" name="Engin_size" min="0.8" max="5.0" step="0.1"
              value={form.Engin_size} onChange={handleChange} />
          </div>

          <div className="slider-group">
            <label>Registration Year: {form.Reg_year}</label>
            <input type="range" name="Reg_year" min="1995" max="2025" step="1"
              value={form.Reg_year} onChange={handleChange} />
          </div>

          <div className="slider-group">
            <label>Miles: {form.Runned_Miles.toLocaleString()}</label>
            <input type="range" name="Runned_Miles" min="0" max="300000" step="1000"
              value={form.Runned_Miles} onChange={handleChange} />
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Calculating...' : 'Estimate Price'}
          </button>
        </form>

        {result && (
          <>
            <div className="result-box">
              <h3>Estimated Price Right Now:</h3>
              <p>{result}</p>
              <h3>Price in the Future:</h3>
            </div>

            {image && (
              <div className="prediction-image-container">
                <img
                  src={`data:image/png;base64,${image}`}
                  alt="Prediction plot"
                  className="prediction-image"
                />
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default App
