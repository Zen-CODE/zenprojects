/*
    Module housing the app server
*/
const port = 3000
const app = require('./app.js')

app.listen(port, () => {
    console.log(`ZenTunez Node API app listening on port ${port}\r`)
})
