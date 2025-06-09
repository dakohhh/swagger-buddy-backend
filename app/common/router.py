from fastapi import APIRouter
from typing import List, Optional
from pydantic import StringConstraints
from typing_extensions import Annotated
VersionType = Annotated[str, StringConstraints(pattern=r"^[1-9]\d*$")]

class VersionRouter(APIRouter):
    def __init__(self, version: VersionType, path: str, tags: Optional[List[str]] = None, *args, **kwargs):
        self._validate_version(version)
        self.version = version
        self.prefix = f"/v{version}/{path}"
        super().__init__(prefix=self.prefix, tags=tags, *args, **kwargs)

    def _validate_version(self, version: str):
        """Validate that version is a string representing a positive integer"""
        if not version.isdigit() or int(version) <= 0:
            raise ValueError(f"Version must be a string representing a positive integer, got '{version}'")