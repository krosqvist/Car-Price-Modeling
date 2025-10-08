const express = require('express')
const cors = require('cors')
const { spawn } = require('child_process')
const path = require('path')
require('dotenv').config()

const app = express()
app.use(cors())
app.use(express.json())
app.use(express.static('dist'))

app.post('/run', (req, res) => {
  const args = [
    req.body.Maker,
    req.body.Genmodel,
    req.body.Gearbox,
    req.body.Fuel_type,
    req.body.Bodytype,
    req.body.Engin_size,
    req.body.Reg_year,
    req.body.km
  ]

  const scriptPath = path.resolve('script.py');
  console.log('Script path:', scriptPath);

  const py = spawn('python3', ['-u', scriptPath, ...args]);

  let output = '';
  let errors = '';

  py.stdout.on('data', (data) => {
    console.log('Python stdout:', data.toString());
    output += data.toString();
  });

  py.stderr.on('data', (data) => {
    console.error('Python stderr:', data.toString());
    errors += data.toString();
  });

  py.on('error', (err) => {
    console.error('Failed to start Python:', err);
    res.status(500).json({ error: 'Failed to start Python', details: err.message });
  });

  py.on('close', (code) => {
    console.log('Python process exited with code', code);
    if (code !== 0) {
      return res.status(500).json({ error: 'Python script failed', details: errors });
    }
    res.json({ result: output.trim() });
  });
});

const PORT = process.env.PORT;
app.listen(PORT, () => console.log(`Server running on ${PORT}`))
