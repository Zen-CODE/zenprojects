// const ZENPLAYER_URL = "http://9.0.0.7:9001/"
const ZENPLAYER_URL = "http://127.0.0.1:9001/"


async function get_response(req, res, endpoint) {
    const response = await fetch(`${ZENPLAYER_URL}/${endpoint}`, 
                           {cache: 'no-cache'});
    const json = await response.json();
    console.log(json);
    return json
};

module.exports.get_response = get_response
