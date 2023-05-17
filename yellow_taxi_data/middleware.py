"""Custom middleware for the application."""
from typing import Callable, Optional

import structlog
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class LogStatusCode(BaseHTTPMiddleware):
    """Log configured status codes."""

    def __init__(
        self, app: FastAPI, *, status_codes: list, logger: Optional[Callable] = None
    ):
        self._logger = logger or structlog.get_logger(__name__).info
        self._status_codes = (
            status_codes if isinstance(status_codes, list) else [status_codes]
        )

        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Log specific status codes.

        Args:
            request: The request object.
            call_next: The next callable.

        Returns:
            The response
        """
        response = await call_next(request)

        body = b""
        async for chunk in response.body_iterator:
            body += chunk

        if response.status_code in self._status_codes:
            self._logger(
                f"Captured status code {response.status_code}",
                status_code=response.status_code,
                body=body.decode("utf-8"),
            )

        return Response(
            content=body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
