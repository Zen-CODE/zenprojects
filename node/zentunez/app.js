// The ZenTunez Node App
const express = require('express')
const app = express()
const port = 3000

module.exports = app

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
    res.send('======== ZenTunez Node ========\r')
  })


app.get('/now_playing', (req, res) => {
    res.send('======== ZenTunez -> Now playing...\r')
})


app.listen(port, () => {
    console.log(`ZenTunez Node API app listening on port ${port}\r`)
})
