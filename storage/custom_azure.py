from storages.backends.azure_storage import AzureStorage
from aizo_backend.settings import STORAGE_ACCOUNT_NAME, STORAGE_ACCOUNT_KEY, STORAGE_AZURE_CONTAINER


class MyAzureStorage(AzureStorage):
    account_name = STORAGE_ACCOUNT_NAME
    account_key = STORAGE_ACCOUNT_KEY
    azure_container = STORAGE_AZURE_CONTAINER
    expiration_secs = None
