from typing import Any, Union
from pathlib import Path
import json


def read_json(path: Union[Path, str]) -> Any:
    with open(path) as f:
        data = json.load(f)
    return data
