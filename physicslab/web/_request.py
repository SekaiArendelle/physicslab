"""Pooled HTTP/HTTPS transport built on ``urllib3``.

``urllib3`` is the package's only runtime HTTP dependency. A thread-safe
connection pool is kept per TLS-verification mode: connections are reused
across requests (keep-alive), which matters for the web iterators that fire
hundreds of requests at the same host.

Requests are single-attempt by design: retries are governed by the caller
(``webutils._run_task``). Redirects are followed (up to a small bound) and
gzip response bodies are decoded automatically.
"""

import json
import ssl

import urllib3
from urllib3 import PoolManager
from urllib3.util.retry import Retry

from physicslab._typing import Union, Dict, Optional, Any

# Single transport attempt (the caller retries), with redirects followed up
# to a small bound. Retrying errors is left to ``webutils._run_task``.
_RETRIES = Retry(connect=0, read=0, other=0, redirect=3)

_SECURE_POOL = PoolManager(retries=_RETRIES)
_INSECURE_POOL = PoolManager(
    retries=_RETRIES,
    cert_reqs=ssl.CERT_NONE,
    assert_hostname=False,
)


def _request(
    domain: str,
    path: str,
    *,
    method: str,
    header: Optional[Dict[str, str]] = None,
    body: Optional[Union[bytes, dict]] = None,
    port: int = 443,
    verify: bool = True,
    timeout: Optional[float] = 30.0,
    use_https: bool = True,
) -> bytes:
    """Perform a single HTTP(S) request and return the decoded response body.

    Args:
        domain: The host name, e.g. ``"physics-api-cn.turtlesim.com"``.
        path: The URL path, e.g. ``"Users/Authenticate"``.
        method: HTTP method, one of ``"GET"`` or ``"POST"``.
        header: Request headers.
        body: Request body. A ``dict`` is JSON-encoded as UTF-8.
        port: TCP port of the server.
        verify: Whether to verify the TLS certificate.
        timeout: Timeout in seconds for the whole request. ``None`` disables it.
        use_https: Whether to use HTTPS instead of HTTP.

    Returns:
        The response body bytes (gzip content is decoded).

    Raises:
        TypeError: Any argument has an invalid type.
        urllib3.exceptions.HTTPError: The request failed at the transport
            level or the server returned an HTTP error status (>= 400).

    """
    if not isinstance(domain, str):
        raise TypeError(
            f"Parameter `domain` must be of type `str`, but got value `{domain}` of type `{type(domain).__name__}`"
        )
    if not isinstance(path, str):
        raise TypeError(
            f"Parameter `path` must be of type `str`, but got value `{path}` of type `{type(path).__name__}`"
        )
    if not isinstance(method, str):
        raise TypeError(
            f"Parameter `method` must be of type `str`, but got value `{method}` of type `{type(method).__name__}`"
        )
    if method not in ("GET", "POST"):
        raise ValueError(
            f"Parameter `method` must be one of ['GET', 'POST'], but got value `{method}`"
        )
    if header is not None and not isinstance(header, dict):
        raise TypeError(
            f"Parameter `header` must be of type `dict` or `None`, but got value `{header}` of type `{type(header).__name__}`"
        )
    if body is not None and not isinstance(body, (bytes, dict)):
        raise TypeError(
            f"Parameter `body` must be of type `bytes`, `dict` or `None`, but got value `{body}` of type `{type(body).__name__}`"
        )
    if not isinstance(port, int):
        raise TypeError(
            f"Parameter `port` must be of type `int`, but got value `{port}` of type `{type(port).__name__}`"
        )
    if not isinstance(verify, bool):
        raise TypeError(
            f"Parameter `verify` must be of type `bool`, but got value `{verify}` of type `{type(verify).__name__}`"
        )
    if not isinstance(timeout, (int, float, type(None))):
        raise TypeError(
            f"Parameter `timeout` must be of type `Optional[float]`, but got value `{timeout}` of type `{type(timeout).__name__}`"
        )
    if not isinstance(use_https, bool):
        raise TypeError(
            f"Parameter `use_https` must be of type `bool`, but got value `{use_https}` of type `{type(use_https).__name__}`"
        )

    scheme = "https" if use_https else "http"
    url = f"{scheme}://{domain}:{port}/{path}"

    if isinstance(body, dict):
        final_body: Optional[bytes] = json.dumps(body).encode("utf-8")
    elif body is None:
        final_body = None
    else:
        final_body = body

    pool = _SECURE_POOL if verify else _INSECURE_POOL
    response = pool.request(
        method,
        url,
        body=final_body,
        headers=header,
        timeout=timeout,
    )
    if response.status >= 400:
        raise urllib3.exceptions.HTTPError(
            f"HTTP {response.status} returned by {method} {url}"
        )
    content = response.data
    if content is None:
        return b""
    return content


def get_https(
    domain: str,
    path: str,
    port: int = 443,
    verify: bool = True,
    timeout: Optional[float] = 30.0,
) -> bytes:
    """Send an HTTPS GET request.

    Args:
        domain: The host name.
        path: The URL path.
        port: TCP port of the server.
        verify: Whether to verify the TLS certificate.
        timeout: Timeout in seconds for the whole request. ``None`` disables it.

    Returns:
        The response body bytes (gzip content is decoded).

    """
    return _request(
        domain,
        path,
        method="GET",
        port=port,
        verify=verify,
        timeout=timeout,
    )


def get_http(
    domain: str,
    path: str,
    port: int = 80,
    timeout: Optional[float] = 30.0,
) -> bytes:
    """Send an HTTP GET request.

    Args:
        domain: The host name.
        path: The URL path.
        port: TCP port of the server.
        timeout: Timeout in seconds for the whole request. ``None`` disables it.

    Returns:
        The response body bytes (gzip content is decoded).

    """
    return _request(
        domain,
        path,
        method="GET",
        port=port,
        timeout=timeout,
        use_https=False,
    )


def post_https(
    domain: str,
    path: str,
    header: Dict[str, str],
    body: Union[bytes, dict],
    port: int = 443,
    verify: bool = True,
    timeout: Optional[float] = 30.0,
) -> dict:
    """Send an HTTPS POST request and parse the JSON response body.

    Args:
        domain: The host name.
        path: The URL path.
        header: Request headers.
        body: Request body. A ``dict`` is JSON-encoded as UTF-8.
        port: TCP port of the server.
        verify: Whether to verify the TLS certificate.
        timeout: Timeout in seconds for the whole request. ``None`` disables it.

    Returns:
        The parsed JSON response body.

    """
    content = _request(
        domain,
        path,
        method="POST",
        header=header,
        body=body,
        port=port,
        verify=verify,
        timeout=timeout,
    )
    return json.loads(content)


def post_multipart(
    domain: str,
    path: str,
    fields: Dict[str, Any],
    port: int = 80,
    timeout: Optional[float] = 60.0,
) -> dict:
    """Send an HTTP multipart/form-data POST request and parse the JSON response.

    Args:
        domain: The host name.
        path: The URL path.
        fields: Form fields. A value is either a plain ``str``, or a tuple of
            ``(filename, data, content_type)`` for a file part, where ``data``
            must already be ``bytes``.
        port: TCP port of the server.
        timeout: Timeout in seconds for the whole request. ``None`` disables it.

    Returns:
        The parsed JSON response body.

    Raises:
        urllib3.exceptions.HTTPError: The request failed at the transport
            level or the server returned an HTTP error status (>= 400).

    """
    if not isinstance(domain, str):
        raise TypeError(
            f"Parameter `domain` must be of type `str`, but got value `{domain}` of type `{type(domain).__name__}`"
        )
    if not isinstance(path, str):
        raise TypeError(
            f"Parameter `path` must be of type `str`, but got value `{path}` of type `{type(path).__name__}`"
        )
    if not isinstance(fields, dict):
        raise TypeError(
            f"Parameter `fields` must be of type `dict`, but got value `{fields}` of type `{type(fields).__name__}`"
        )
    if not isinstance(port, int):
        raise TypeError(
            f"Parameter `port` must be of type `int`, but got value `{port}` of type `{type(port).__name__}`"
        )
    if not isinstance(timeout, (int, float, type(None))):
        raise TypeError(
            f"Parameter `timeout` must be of type `Optional[float]`, but got value `{timeout}` of type `{type(timeout).__name__}`"
        )

    url = f"http://{domain}:{port}/{path}"
    response = _SECURE_POOL.request("POST", url, fields=fields, timeout=timeout)
    if response.status >= 400:
        raise urllib3.exceptions.HTTPError(
            f"HTTP {response.status} returned by POST {url}"
        )
    return json.loads(response.data)
