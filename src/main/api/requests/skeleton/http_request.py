from dataclasses import dataclass
from typing import Protocol, Dict, Callable

from src.main.api.requests.skeleton.endpoint import Endpoint


@dataclass
class HttpRequest(Protocol):
    request_spec: Dict[str, str]
    endpoint: Endpoint
    response_spec: Callable
