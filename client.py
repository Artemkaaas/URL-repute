from jsonrpclib import Server
server = Server('http://localhost:8184')
result = server.get_url_repute('http://www.google.com/dropbox/dpbx/index.php/hgh')
print result
