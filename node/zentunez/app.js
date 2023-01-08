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


con_to_time = (seconds) => {
    const d = Math.floor(seconds / (3600*24))
    const h = Math.floor(seconds % (3600*24) / 3600)
    const m = Math.floor(seconds % 3600 / 60)
    const s = Math.floor(seconds % 60)

    const dDisplay = d > 0 ? d + (d == 1 ? " day, " : " days, ") : ""
    const hDisplay = h > 0 ? h + (h == 1 ? " hour, " : " hours, ") : ""
    const mDisplay = m > 0 ? m + (m == 1 ? " minute, " : " minutes, ") : ""
    const sDisplay = s > 0 ? s + (s == 1 ? " second" : " seconds") : ""
    return dDisplay + hDisplay + mDisplay + sDisplay
}

app.get('/sysinfo*', async (req, res) => {
    const json = {
        "Arch" : os.arch(),
        "CPU's": os.cpus(),
        "Free memory": (os.freemem() / (1024 ** 3)).toString() + " GB",
        "Total memory": (os.totalmem() / (1024 ** 3)).toString() + " GB",
        "Load average (1, 5, 15min)": os.loadavg(),
        "Platform": os.platform(),
        "Release": os.release(),
        "Uptime": con_to_time(os.uptime())
    }
    res.json(json)
})
