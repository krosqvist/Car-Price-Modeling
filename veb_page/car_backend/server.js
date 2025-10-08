const express = require('express')
const cors = require('cors')
const { spawn } = require('child_process')

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

  const py = spawn('python3', ['script.py', ...args])

  let dataString = ''
  py.stdout.on('data', (data) => (dataString += data.toString()))

  py.on('close', () => {
    res.json({ result: dataString.trim() })
  })
})

const PORT = process.env.PORT;
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`))
