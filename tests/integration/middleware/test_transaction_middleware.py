import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.infrastructure.persistence.transaction import set_current_session
from tests.integration.utils.transaction_manager import test_transaction_manager

logger = logging.getLogger(__name__)


class TransactionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        transaction_token = request.headers.get("x-transaction-token")
        if transaction_token:
            session = test_transaction_manager.get_session(transaction_token)

            if session:
                set_current_session(session)
                logger.debug(f"Set transaction context for token: {transaction_token}")
            else:
                logger.warning(f"No session found for transaction token: {transaction_token}")

        return await call_next(request)
