from jsonrpclib import Server

server = Server('http://localhost:8817')
#OpenPhish
result = server.get_url_repute('northreefgroup1.co.za/wp-content/themes/doc/index.htm')
#Alex
#result = server.get_url_repute('yahoo.com')
#Phishtank
#result = server.get_url_repute('submarin.promocoess.com.br/ds')
print result
