// The ZenTunez Node App
const express = require('express')
const app = express()
const port = 3000
const ZENPLAYER_URL = "http://127.0.0.1:9001/"

module.exports = app

// respond with "hello world" when a GET request is made to the homepage
app.get('/', (req, res) => {
    res.send('======== ZenTunez Node ========\r')
  })


app.get('/now_playing', (req, res) => {
    res.send('======== ZenTunez -> Now playing...\r');
    fetch(`${ZENPLAYER_URL}/zenplaylist/get_current_info`, 
                           {cache: 'no-cache'})
    .then((response) => response.json())
    .then((data) => console.log(data));                           

})


app.listen(port, () => {
    console.log(`ZenTunez Node API app listening on port ${port}\r`)
})
