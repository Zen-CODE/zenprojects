#! bash
echo "Retrieving 'Now playing' list..."
curl http://127.0.0.1:3000/get_play_pause | json_pp
