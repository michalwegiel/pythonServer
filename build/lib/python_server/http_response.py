PROTOCOL_VERSION: str = "HTTP/1.1"
CONTENT_TYPE: str = "Content-Type: text/html"
SERVER_TIMING: str = "Server-Timing: miss, db;dur=50, app;dur=50"


class HTTPResponse:
    def __init__(self, status_code: int, status_info: str, content: str):
        self.protocol_version_with_status = (
            f"{PROTOCOL_VERSION} {status_code} {status_info}"
        )
        self.content = content

    def produce_response(self) -> bytes:
        return (
            f"{self.protocol_version_with_status}\r\n{SERVER_TIMING}\r\n"
            f"{CONTENT_TYPE}\r\nContent-Length:{len(self.content)}\r\n\r\n"
            f"{self.content}\r\n\r\n".encode()
        )
