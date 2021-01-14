from typing import TYPE_CHECKING
import config  # imported for indirect use

if TYPE_CHECKING:
    from cmyui import (AsyncSQLPoolWrapper, Version)

__all__ = ("db", "version")

db: "AsyncSQLPoolWrapper"
version: "Version"

cache = {
    "bcrypt": {}
}