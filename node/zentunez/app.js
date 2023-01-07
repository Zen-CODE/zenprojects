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


app.get('/*', async (req, res) => {
    const endpoint = req.url.substring(1)
    console.log(`Forwarding call to ${endpoint}`)
    const json = await get_response(req, res, endpoint)
    res.append('json', json)
    res.send(JSON.stringify(json))
})
