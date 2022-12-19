// The ZenTunez Node App
const express = require('express')
const app = express()
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

app.get('/get_current_info', async (req, res) => {
    return await get_response(req, res, "zenplaylist/get_current_info")
})

app.get('/get_playlist', async (req, res) => {
    return await get_response(req, res, "zenplaylist/get_playlist")
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
