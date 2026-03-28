import http.client

conn = http.client.HTTPSConnection("dev-lgjx7zr734kfjmv1.us.auth0.com")

payload = "{\"client_id\":\"15NJwoVqpcxtqEjR9T7SiOoXXx61vj8G\",\"client_secret\":\"uK1vkpm4E7TlJbpSX0zlkTxtLnUxqrNKooLL010DalLhz2DeRzbOL0UyGJaNFF4T\",\"audience\":\"https://api.wernipedia.de/\",\"grant_type\":\"client_credentials\"}"

headers = { 'content-type': "application/json" }

conn.request("POST", "/oauth/token", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))