// The ZenTunez Node App
const express = require('express')
const { reset } = require('nodemon')
const app = express()
const port = 3000
const ZENPLAYER_URL = "http://127.0.0.1:9001/"

module.exports = app

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
    res.send('======== ZenTunez Node ========\r')
  })


app.get('/now_playing', async (req, res) => {
    // res.send('======== ZenTunez -> Now playing...\r');
    response = await fetch(`${ZENPLAYER_URL}/zenplaylist/get_current_info`, 
                           {cache: 'no-cache'});
    const json = await response.json();
    console.log(json);
    res.json(json)
})


app.listen(port, () => {
    console.log(`ZenTunez Node API app listening on port ${port}\r`)
})
