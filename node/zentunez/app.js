// The ZenTunez Node App
const express = require('express')
const app = express()
const get_response = require("./utils.js").get_response
const os = require('os')

module.exports = app

/*
    Return the Title page of the ZenTunez node app.`
*/
app.get('/', (req, res) => {
    res.send('======== ZenTunez Node ========\r\n' +
            'This is ZenTunez node app. Please see the "curls" folder for ' +
            'the available commands.\r\n')
  })


app.get('/zen*', async (req, res) => {
    const endpoint = req.url.substring(1)
    console.log(`Forwarding call to ${endpoint}`)
    const json = await get_response(req, res, endpoint)
    res.json(json)
})


app.get('/sysinfo*', async (req, res) => {
    const json = {
        "Arch" : os.arch(),
        "CPU's": os.cpus(),
        "Free memory": (os.freemem() / (1024 ** 3)).toString() + " GB",
        "Load average (1, 5 15min)": os.loadavg()
    }
    res.json(json)
})
