// The ZenTunez Node App
const express = require('express')
const { reset } = require('nodemon')
const app = express()
const port = 3000
const ZENPLAYER_URL = "http://127.0.0.1:9001/"

module.exports = app


async function get_response(req, res, endpoint) {
    response = await fetch(`${ZENPLAYER_URL}/${endpoint}`, 
                           {cache: 'no-cache'});
    const json = await response.json();
    console.log(json);
    return res.json(json)
}

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



app.listen(port, () => {
    console.log(`ZenTunez Node API app listening on port ${port}\r`)
})
