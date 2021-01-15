# -*- coding: utf-8 -*-

from typing import TYPE_CHECKING

import config  # imported for indirect use

if TYPE_CHECKING:
    from cmyui import AsyncSQLPool, Version

__all__ = ('db', 'version')

db: 'AsyncSQLPool'
version: 'Version'

cache = {
    'bcrypt': {}
}
