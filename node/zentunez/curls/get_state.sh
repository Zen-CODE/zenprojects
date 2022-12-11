#! bash
echo "Retrieving state..."
curl http://127.0.0.1:3000/get_state | json_pp
