
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class Application:
    """
    Creates a new Ghost Instance based on the commands passed in.
    """
    
    ghost: Any

    events: Any

    command: str

    command_map: Dict[Any, Any] = {}
    
