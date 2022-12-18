// The ZenTunez Node App
const express = require('express')
const app = express()
const port = 3000
const get_response = require("./utils.js").get_response

module.exports = app



/*
    Return the Title page of the ZenTunez node app.`
*/
app.get('/', (req, res) => {
    res.send('======== ZenTunez Node ========\r\n' +
            'This is ZenTunez node app. Please see the "curls" folder for ' +
            'the available commands.\r\n')
  })

app.get('/now_playing', async (req, res) => {
    return await get_response(req, res, "zenplaylist/get_current_info")
})

app.get('/get_state', (req, res) => {
    return get_response(req, res, "/zenplayer/get_state")
})

app.get('/get_play_pause', (req, res) => {
    return get_response(req, res, "/zenplayer/play_pause")
})

app.get('/get_track_meta', (req, res) => {
    return get_response(req, res, "/zenplayer/get_track_meta")
})

app.listen(port, () => {
    console.log(`ZenTunez Node API app listening on port ${port}\r`)
})
