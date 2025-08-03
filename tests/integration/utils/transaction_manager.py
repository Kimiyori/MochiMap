from sqlalchemy.ext.asyncio import AsyncSession


class TransactionManager:
    def __init__(self) -> None:
        self._transactions: dict[str, AsyncSession] = {}

    def create_transaction(self, transaction_token: str, session: AsyncSession) -> None:
        self._transactions[transaction_token] = session

    def get_session(self, transaction_token: str) -> AsyncSession | None:
        return self._transactions.get(transaction_token)

    def remove_transaction(self, transaction_token: str) -> None:
        self._transactions.pop(transaction_token, None)

    def clear_all(self) -> None:
        self._transactions.clear()

    def get_all_transactions(self) -> dict[str, AsyncSession]:
        return self._transactions

test_transaction_manager = TransactionManager()
