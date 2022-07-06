import json
# import http.client

# conn = http.client.HTTPSConnection("coffeeplace-app.us.auth0.com")

# payload = "{\"client_id\":\"Sn7NpJ0ooLVUdS9GIqOAip5rac1ppPZv\",\"client_secret\":\"3I0PcTW-oMF5ucwSmskdgLaFCJQ71tc6LzGwAjoKEuQUZsagYo9xEacRqALKK8vO\",\"audience\":\"coffeeplace\",\"grant_type\":\"client_credentials\"}"

# headers = { 'content-type': "application/json" }

# conn.request("POST", "/oauth/token", payload, headers)

# res = conn.getresponse()
# data = res.read()

# print(data.decode("utf-8"))

data = '{"name": "Water", "color": "blue", "parts": 1}'

print(json.loads(data))