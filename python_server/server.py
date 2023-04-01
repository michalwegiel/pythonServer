import socket
import threading
import uuid
from multiprocessing import Process

from python_server.request_handler import handle_request

DEFAULT_TCP_CLIENT_BUFFER_SIZE: int = 1_000_000  # 1 MB


class TCPServer:
    """
    A TCP python_server that listens for incoming connections and handles them in separate threads.

    Attributes
    ----------
    host: str
        The host address to bind the python_server to.
    port: int
        The port number to bind the python_server to.
    server: socket.socket
        The socket object representing python_server.

    Examples
    --------
    - python_server = TCPServer(name="python_server", host_ip="127.0.0.1", port=5050)
      python_server.start()
    """

    host: str
    port: int
    server: socket.socket
    _is_server_active: bool
    _server_process: Process
    _clients: dict[uuid.UUID, threading.Thread]

    def __init__(self, host: str, port: int) -> None:
        """
        Initializes a new TCPServer instance with the specified host and port.

        Parameters
        ----------
        host: str
            The host address to bind the python_server to.
        port: int
            The port number to bind the python_server to.
        """
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._is_server_active = False
        self._server_process = Process(target=self._start, daemon=False)
        self._clients = {}
        self.server.bind((self.host, self.port))

    def start(self) -> None:
        """
        Starts a python_server process that listens for incoming connections and handles each connection in a separate thread.
        """
        if not self._is_server_active:
            print("Starting python_server process...")
            self._is_server_active = True
            self._server_process.start()
        else:
            print("Server is already started!")

    def stop(self) -> None:
        """Stops the python_server."""
        if self._is_server_active:
            self._is_server_active = False
            self._server_process.kill()
            print("Server has been stopped.")
            self._server_process = Process(target=self._start, daemon=False)
        else:
            print("Could not stop the python_server. Server is not running.")

    def _start(self) -> None:
        """Internal method used as a target for a python_server process."""
        self.server.listen()
        print(f"Server listening on http://{self.host}:{self.port}")
        while self._is_server_active:
            try:
                client_socket, client_address = self.server.accept()
            except socket.error as err:
                print(
                    f"Error occurred while trying to create a new connection [{err}]. "
                    f"Waiting for another connection..."
                )
                continue
            print(f"New connection from {client_address}")
            task_id = uuid.uuid4()
            client_thread = threading.Thread(
                target=self._handle_client, args=(client_socket, task_id), daemon=True
            )
            self._clients[task_id] = client_thread
            client_thread.start()

    def _handle_client(self, client_socket: socket.socket, task_id: uuid.UUID) -> None:
        """
        Handles the client connection by receiving messages and, if the echo parameter is set,
        sending them back to the client.

        Parameters
        ----------
        client_socket: socket.socket
            The socket object for the client connection.
        task_id: uuid.UUID
            Client thread id.
        """
        while True:
            try:
                data = client_socket.recv(DEFAULT_TCP_CLIENT_BUFFER_SIZE)
            except ConnectionResetError:
                print("An existing connection was forcibly closed by the remote host")
                break
            except socket.error as err:
                print(f"Error occurred while handling client request [{err}]. ")
                break
            if not data:
                break
            print(f"Received data: {data!r}")
            response = handle_request(data)
            client_socket.sendall(response)
        self._disconnect_client(client_socket, task_id)

    def _disconnect_client(
        self, client_socket: socket.socket, task_id: uuid.UUID
    ) -> None:
        """
        Closes the client socket and cancels the client thread.

        Parameters
        ----------
        client_socket: socket.socket
            The socket object for the client connection.
        task_id: uuid.UUID
            Client thread id.
        """
        client_socket.close()
        del self._clients[task_id]
        print("Client disconnected")
