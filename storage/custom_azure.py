from storages.backends.azure_storage import AzureStorage
from aizo_backend.settings import STORAGE_INFO


class MyAzureStorage(AzureStorage):
    account_name = STORAGE_INFO["account_name"]
    account_key = STORAGE_INFO["account_key"]
    azure_container = STORAGE_INFO["azure_container"]
    expiration_secs = None
