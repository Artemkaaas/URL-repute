from jsonrpclib import Server

server = Server('http://localhost:8188')
result = server.get_url_repute('http://it-bonus.cf/cartasi/cartasi.php')
print result
