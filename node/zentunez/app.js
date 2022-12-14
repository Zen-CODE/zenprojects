// The ZenTunez Node App
const express = require('express')
const { reset } = require('nodemon')
const app = express()
const port = 3000
// import get_response from './utils.mjs'
const utils = require("./utils.js")


module.exports = app



// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
    res.send('======== ZenTunez Node ========\r')
  })

app.get('/now_playing', async (req, res) => {
    // res.send('======== ZenTunez -> Now playing...\r');
    return get_response(req, res, "zenplaylist/get_current_info")
})

app.get('/get_state', (req, res) => {
    return get_response(req, res, "/zenplayer/get_state")
})

app.get('/get_play_pause', (req, res) => {
    return get_response(req, res, "/zenplayer/play_pause")
})

app.listen(port, () => {
    console.log(`ZenTunez Node API app listening on port ${port}\r`)
})
