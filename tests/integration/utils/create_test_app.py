from main import create_app
from tests.integration.middleware.test_transaction_middleware import TransactionMiddleware


def create_test_app():
    app = create_app()
    app.add_middleware(TransactionMiddleware)
    return app
