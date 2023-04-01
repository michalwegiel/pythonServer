from enum import Enum


class HTTPResponseCode(Enum):
    OK: tuple[int, str] = (200, "OK")
    CREATED: tuple[int, str] = (201, "Created")
    ACCEPTED: tuple[int, str] = (202, "Accepted")
    NO_CONTENT: tuple[int, str] = (204, "No Content")
    MULTIPLE_CHOICES: tuple[int, str] = (300, "Multiple Choices")
    MOVED_PERMANENTLY: tuple[int, str] = (301, "Moved Permanently")
    FOUND: tuple[int, str] = (302, "Found")
    SEE_OTHER: tuple[int, str] = (303, "See Other")
    NOT_MODIFIED: tuple[int, str] = (304, "Not Modified")
    TEMPORARY_REDIRECT: tuple[int, str] = (307, "Temporary Redirect")
    PERMANENT_REDIRECT: tuple[int, str] = (308, "Permanent Redirect")
    BAD_REQUEST: tuple[int, str] = (400, "Bad Request")
    UNAUTHORIZED: tuple[int, str] = (401, "Unauthorized")
    FORBIDDEN: tuple[int, str] = (403, "Forbidden")
    NOT_FOUND: tuple[int, str] = (404, "Not Found")
    METHOD_NOT_ALLOWED: tuple[int, str] = (405, "Method Not Allowed")
    NOT_ACCEPTABLE: tuple[int, str] = (406, "Not Acceptable")
    CONFLICT: tuple[int, str] = (409, "Conflict")
    UNSUPPORTED_MEDIA_TYPE: tuple[int, str] = (415, "Unsupported Media Type")
    INTERNAL_SERVER_ERROR: tuple[int, str] = (500, "Internal Server Error")
    NOT_IMPLEMENTED: tuple[int, str] = (501, "Not Implemented")
    BAD_GATEWAY: tuple[int, str] = (502, "Bad Gateway")
    SERVICE_UNAVAILABLE: tuple[int, str] = (503, "Service Unavailable")
    GATEWAY_TIMEOUT: tuple[int, str] = (504, "Gateway Timeout")
    HTTP_VERSION_NOT_SUPPORTED: tuple[int, str] = (505, "HTTP Version Not Supported")


class HTTPResponse:
    """
    Represents an HTTP response message with the specified status code, status
    information, and content.

    Attributes
    ----------
    PROTOCOL_VERSION : str
        The protocol version for the HTTP response message.
    CONTENT_TYPE : str
        The content type for the HTTP response message.
    SERVER_TIMING : str
        The server timing information for the HTTP response message.

    Methods
    -------
    produce_response() -> bytes
        Produces a bytes representation of the HTTP response message.
    """

    PROTOCOL_VERSION: str = "HTTP/1.1"
    CONTENT_TYPE: str = "Content-Type: text/html"
    SERVER_TIMING: str = "Server-Timing: miss, db;dur=50, app;dur=50"

    def __init__(self, status_code_and_info: tuple[int, str], content: str) -> None:
        """
        Initializes a new HTTPResponse object with the specified status code,
        status information, and content.

        Parameters
        ----------
        status_code_and_info: tuple[int, str]
            Object representing the HTTP status code for the response with the status information (e.g. 200, "OK")
        content : str
            The content to be included in the response.
        """
        self.status_code, self.status_info = status_code_and_info
        self.status_line: str = (
            f"{self.PROTOCOL_VERSION} {self.status_code} {self.status_info}"
        )
        self.content: str = content

    def produce_response(self) -> bytes:
        """
        Produces a bytes representation of the HTTP response message.

        Returns
        -------
        bytes
            The HTTP response message as a bytes object.
        """
        response: str = (
            f"{self.status_line}\r\n{self.SERVER_TIMING}\r\n"
            f"{self.CONTENT_TYPE}\r\nContent-Length:{len(self.content)}\r\n\r\n"
            f"{self.content}\r\n\r\n"
        )
        return response.encode()

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
            f"status_info='{self.status_info}', content='{self.content}')"
        )
