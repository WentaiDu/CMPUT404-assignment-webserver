import socketserver
class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()

        request = self.data.decode("utf-8")
        headers = request.split('\n')
        request_method,filename,_ = headers[0].split()
        if not self.method_check(request_method):
            self.handle_405()
        else:
            response = 'HTTP/1.1 200 OK\r\n'
            if filename[-1] != '/' and '.' not in filename:
                filename = 'http://127.0.0.1:8080'+filename+'/'
                self.handle_301(filename)
                filename=None
            elif filename == '/':
                filename = './www/index.html'
            elif '.' not in filename:
                filename = './www'+filename+'/index.html'
            else:
                filename='./www'+filename


            if filename is not None:
		
                if '.html' in filename or '.css' in filename:
                    try:
                        text=self.file_open(filename)

                        if '.html' in filename:
                            file_type = 'text/html'
                        elif '.css' in filename:
                            file_type = 'text/css'

                        response = response + 'content-type: '+ file_type + '\r\n\r\n' + text

                    except:
                        response = 'HTTP/1.1 404 Not Found\r\n\r\n 404 Not Found'

                    finally:

                        self.response(response)

                else:

                    self.handle_404()

            else:
                self.handle_405()
    def file_open(self,filename):
        file = open(filename)
        text = file.read()
        file.close()
        return text

    def file_check(self,response,text,filename):
        
        if '.css' in filename:
            mine = 'text/css'
        elif '.html' in filename:
            mine = 'text/html'

        response = response + 'content-type: '+ mime + '\r\n\r\n' + text
        return response



    #def handle_200(self):
    #    response = 'HTTP/1.1 200 OK\r\n'
	#return response

    def handle_404(self):
        response = "HTTP/1.1 404 Not Found\r\n\r\n 404 Not Found"
        self.response(response)
    def handle_405(self):
        response = 'HTTP/1.1 405 Method Not Allowed\r\n'
        self.response(response)
    def handle_301(self, URI):
        response = "HTTP/1.1 301 Moved Permanently\r\nLocation:"+ URI+"\r\n"
        self.response(response)

    def sendResponse(self, MIMA_type, thedata):
        response = 'HTTP/1.1 200 OK\r\n'+ 'Content-type: '+ MIMA_type +'\r\n' + thedata
        self.response(response)

    def response(self,msg):
        self.request.sendall(bytearray(msg, 'utf-8'))



    def method_check(self,request_method):
        if request_method == "GET":
            return True
        else:
            return False

    def check_file(self, filename):
        if filename[-1] != '/' and '.' not in filename:
            filename = 'http://127.0.0.1:8080'+filename+'/'
            #self.request.sendall(bytearray('HTTP/1.1 301 Moved Permanently\r\nLocation:' + filename + '\r\n', 'utf-8'))
            self.handle_301(filename)
            return None
        if filename == '/':
            filename = './www/index.html'
            return filename
        if '.' not in filename:
            filename = './www'+filename+'/index.html'
            return filename
        return './www'+filename


if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 8080

    socketserver.TCPServer.allow_reuse_address = True

    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    server.serve_forever()
