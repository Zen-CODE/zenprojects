#! bash
echo "Retrieving track meta..."
curl http://127.0.0.1:3000/get_track_meta | json_pp
