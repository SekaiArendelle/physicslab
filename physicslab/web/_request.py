"""Provide request related functionality."""

import ssl
import json
import urllib.request
from physicslab._typing import Union, Dict


def get_http(domain: str, path: str, port: int = 80) -> bytes:
    """Get http."""
    if not isinstance(domain, str):
        raise TypeError(
            f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`"
        )
    if not isinstance(path, str):
        raise TypeError(
            f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`"
        )
    if not isinstance(port, int):
        raise TypeError(
            f"Parameter port must be of type `int`, but got value {port} of type `{type(port).__name__}`"
        )

    url = f"http://{domain}:{port}/{path}"
    req = urllib.request.urlopen(url)

    return req.read()


def get_https(domain: str, path: str, port: int = 443, verify: bool = True) -> bytes:
    """Get https."""
    if not isinstance(domain, str):
        raise TypeError(
            f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`"
        )
    if not isinstance(path, str):
        raise TypeError(
            f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`"
        )
    if not isinstance(port, int):
        raise TypeError(
            f"Parameter port must be of type `int`, but got value {port} of type `{type(port).__name__}`"
        )
    if not isinstance(verify, bool):
        raise TypeError(
            f"Parameter verify must be of type `bool`, but got value {verify} of type `{type(verify).__name__}`"
        )

    url = f"https://{domain}:{port}/{path}"
    if verify:
        req = urllib.request.urlopen(url)
    else:
        context = ssl._create_unverified_context()
        req = urllib.request.urlopen(url, context=context)

    return req.read()


def post_http(
    domain: str,
    path: str,
    header: Dict[str, str],
    body: bytes,
    port: int = 80,
) -> dict:
    """Execute the post http routine."""
    if not isinstance(domain, str):
        raise TypeError(
            f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`"
        )
    if not isinstance(path, str):
        raise TypeError(
            f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`"
        )
    if not isinstance(header, dict):
        raise TypeError(
            f"Parameter header must be of type `dict`, but got value {header} of type `{type(header).__name__}`"
        )
    if not isinstance(body, (bytes, dict)):
        raise TypeError(
            f"Parameter body must be of type `bytes` or `dict`, but got value {body} of type `{type(body).__name__}`"
        )
    if not isinstance(port, int):
        raise TypeError(
            f"Parameter port must be of type `int`, but got value {port} of type `{type(port).__name__}`"
        )

    if isinstance(body, dict):
        final_body = json.dumps(body).encode("utf-8")
    else:
        final_body = body

    url = f"http://{domain}:{port}/{path}"
    req = urllib.request.Request(url, data=final_body, method="POST")
    req.headers = header

    with urllib.request.urlopen(req) as response:
        if response.info().get("Content-Encoding") == "gzip":
            import gzip

            content = gzip.decompress(response.read())
        else:
            content = response.read()
        return json.loads(content)


def post_https(
    domain: str,
    path: str,
    header: Dict[str, str],
    body: Union[bytes, dict],
    port: int = 443,
    verify: bool = True,
) -> dict:
    """Execute the post https routine."""
    if not isinstance(domain, str):
        raise TypeError(
            f"Parameter domain must be of type `str`, but got value {domain} of type `{type(domain).__name__}`"
        )
    if not isinstance(path, str):
        raise TypeError(
            f"Parameter path must be of type `str`, but got value {path} of type `{type(path).__name__}`"
        )
    if not isinstance(header, dict):
        raise TypeError(
            f"Parameter header must be of type `dict`, but got value {header} of type `{type(header).__name__}`"
        )
    if not isinstance(body, (bytes, dict)):
        raise TypeError(
            f"Parameter body must be of type `bytes` or `dict`, but got value {body} of type `{type(body).__name__}`"
        )
    if not isinstance(port, int):
        raise TypeError(
            f"Parameter port must be of type `int`, but got value {port} of type `{type(port).__name__}`"
        )

    context = None
    if verify == False:
        context = ssl._create_unverified_context()

    if isinstance(body, dict):
        final_body = json.dumps(body).encode("utf-8")
    else:
        final_body = body

    url = f"https://{domain}:{port}/{path}"
    req = urllib.request.Request(url, data=final_body, method="POST")
    req.headers = header

    with urllib.request.urlopen(req, context=context) as response:
        if response.info().get("Content-Encoding") == "gzip":
            import gzip

            content = gzip.decompress(response.read())
        else:
            content = response.read()
        return json.loads(content)
