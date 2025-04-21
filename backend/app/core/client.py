import httpx

class HTTPClient:
    client: httpx.Client = None

    def get_client(cls):
        if cls.client is None:
            cls.client = httpx.Client()
        return cls.client