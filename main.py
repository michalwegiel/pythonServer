from python_server import TCPServer

if __name__ == "__main__":
    server = TCPServer("127.0.0.1", 8000)
    server.start()
