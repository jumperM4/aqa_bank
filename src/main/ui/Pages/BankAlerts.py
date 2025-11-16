from enum import Enum


class BankAlert(Enum):
    USER_CREATED_SUCCESFULLY = "User created successfully!"
    USER_CREATED_ACCOUNT_SUCCESSFULLY = "New Account Created! Account Number:"

    USER_DEPOSITED_MONEY_WITH_NO_ACCOUNT = "Please select an account."
    USER_DEPOSITED_MONEY_WITH_EMPTY_AMOUNT_FIELD = "Please enter a valid amount."
    USER_DEPOSITED_SUCCESSFULLY = "Successfully deposited"

    USER_TRANSFERRED_MONEY_SUCCESSFULLY = "Successfully transferred"
    USER_TRANSFERRED_MONEY_SUCCESSFULLY_AGAIN = "Transfer of $5 successful"
    USER_TRANSFERRED_MONEY_WITH_EMPTY_FIELDS = "Please fill all fields and confirm."
    USER_TRANSFERRED_MONEY_WITH_FILLED_FIELDS_AND_NO_CONFIRM_CHECK = "Please fill all fields and confirm."
    USER_TRANSFERRED_INSUFFICIENT_FUNDS = "Error: Invalid transfer: insufficient funds or invalid accounts"
    USER_TRANSFERRED_MONEY_AGAIN_FAILED = "Transfer failed: Please try again."

    USERNAME_UPDATED_SUCCESSFULLY = "Name updated successfully!"
    USERNAME_FIELD_REQUIRES_VALID_NAME = "Please enter a valid name."

    def __init__(self, message: str):
        self._message = message

    @property
    def message(self) -> str:
        return self._message

