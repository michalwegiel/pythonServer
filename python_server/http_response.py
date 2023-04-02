from enum import Enum


class HTTPResponseCode(Enum):
    """Enum class with predefined HTTP response codes"""
    OK: int = 200
    CREATED: int = 201
    ACCEPTED: int = 202

    TEMPORARY_REDIRECT: int = 307
    PERMANENT_REDIRECT: int = 308

    BAD_REQUEST: int = 400
    UNAUTHORIZED: int = 401
    FORBIDDEN: int = 403
    NOT_FOUND: int = 404
    METHOD_NOT_ALLOWED: int = 405

    INTERNAL_SERVER_ERROR: int = 500
    NOT_IMPLEMENTED: int = 501
    BAD_GATEWAY: int = 502
    SERVICE_UNAVAILABLE: int = 503
    GATEWAY_TIMEOUT: int = 504
    HTTP_VERSION_NOT_SUPPORTED: int = 505


class HTTPResponse:
    """
    Represents an HTTP response message with the specified status code, status
    information, and content.

    Attributes
    ----------
    PROTOCOL_VERSION : str
        The protocol version for the HTTP response message.
    SERVER_TIMING : str
        The server timing information for the HTTP response message.

    Methods
    -------
    produce_response() -> bytes
        Produces a bytes representation of the HTTP response message.
    """

    PROTOCOL_VERSION: str = "HTTP/1.1"
    SERVER_TIMING: str = "Server-Timing: miss, db;dur=50, app;dur=50"

    def __init__(
        self,
        status_code: int,
        status_info: str = "",
        content_type: str = "text/html",
        content: str | bytes = "",
    ) -> None:
        """
        Initializes a new HTTPResponse object with the specified status code,
        status information, and content.

        Parameters
        ----------
        status_code: int
            Http status code
        status_info: str
            Http status info e.g. "OK"
        content : str
            The content to be included in the response.
        """
        self.status_code, self.status_info = status_code, status_info
        self.status_line: str = (
            f"{self.PROTOCOL_VERSION} {self.status_code} {self.status_info}"
        )
        self.content_type = f"Content-Type: {content_type}"
        self.content = content

    def produce_response(self) -> bytes:
        """
        Produces a bytes representation of the HTTP response message.

        Returns
        -------
        bytes
            The HTTP response message as a bytes object.
        """
        if not isinstance(self.content, bytes):
            response: str = (
                f"{self.status_line}\r\n{self.SERVER_TIMING}\r\n"
                f"{self.content_type}\r\nContent-Length:{len(self.content)}\r\n\r\n"
                f"{self.content}\r\n\r\n"
            )
            return response.encode()
        header = (
            f"{self.status_line}\r\n{self.SERVER_TIMING}\r\n"
            f"{self.content_type}\r\nContent-Length:{len(self.content)}\r\n\r\n"
        )
        ending = "\r\n\r\n"
        return header.encode() + self.content + ending.encode()

    def __repr__(self) -> str:
        """
        Returns a string representation of the HTTPResponse object.

        Returns
        -------
        str
            A string representation of the HTTPResponse object.
        """
        return (
            f"HTTPResponse(status_code={self.status_code}, "
            f"status_info='{self.status_info}', content='{self.content!r}')"
        )
