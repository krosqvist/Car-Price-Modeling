const express = require('express')
const { spawn } = require('child_process')

const app = express()

app.get('/', (req, res) => {
  res.send(`
    <html>
      <body style="font-family: sans-serif; text-align: center; margin-top: 100px;">
        <h2>Test Python Calling</h2>
        <form action="/run" method="get">
          <input type="text" name="name" placeholder="Enter input">
          <button type="submit">Run python</button>
        </form>
      </body>
    </html>
  `)
})

app.get('/run', (req, res) => {
  const arg = req.query.name

  // Run Python with one argument
  const py = spawn('python3', ['script.py', arg])

  let dataString = ''
  py.stdout.on('data', data => dataString += data.toString())
  console.log(dataString)

  py.on('close', () => {
    res.send(`
      <html>
        <body style="font-family: sans-serif; text-align: center; margin-top: 100px;">
          <h2>Python Output:</h2>
          <p>${dataString}</p>
          <a href="/">Back</a>
        </body>
      </html>
    `)
  })
})

const PORT = 3001
app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`))
