
# from storages.backends. import AzureStorage
from storages.backends.azure_storage import AzureStorage

class AzureMediaStorage(AzureStorage):
    account_name = 'grinmovestorage' # Must be replaced by your <storage_account_name>
    account_key = 'vUv29YNX5pi4hosGE1gfvuH+tZfCz/wiq589er4JTIb0iWxAoCVtqOvmUB29yekpwXXaCOYZd3nI+AStF5vmOw==' # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None

class AzureStaticStorage(AzureStorage):
    account_name = 'grinmovestorage' # Must be replaced by your storage_account_name
    account_key = 'vUv29YNX5pi4hosGE1gfvuH+tZfCz/wiq589er4JTIb0iWxAoCVtqOvmUB29yekpwXXaCOYZd3nI+AStF5vmOw==' # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None