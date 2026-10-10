from tenacity import retry, wait_exponential, stop_after_attempt, retry_if_exception_type
import requests

api_retry = retry(
    wait=wait_exponential(multiplier=1, min=2, max=10),
    stop=stop_after_attempt(3),
    retry=retry_if_exception_type((requests.exceptions.RequestException, ConnectionError, TimeoutError)),
    reraise=True
)
