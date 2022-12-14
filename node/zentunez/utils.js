import { builtinModules } from "module";
import { REPL_MODE_SLOPPY } from "repl";

const ZENPLAYER_URL = "http://127.0.0.1:9001/"

async function get_response(req, res, endpoint) {
    response = await fetch(`${ZENPLAYER_URL}/${endpoint}`, 
                           {cache: 'no-cache'});
    const json = await response.json();
    console.log(json);
    return res.json(json)
}

module.exports = get_response

// export {get_response}
