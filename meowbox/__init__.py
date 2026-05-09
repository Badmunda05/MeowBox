# -*- coding: utf-8 -*-
"""
MeowBox — Permanent File Hosting Python Library
Repo   : https://github.com/Badmunda05/MeowBox
Author : @BadmundaXd

─────────────────────────────────────────────
Quick Start (Sync)
─────────────────────────────────────────────

    from meowbox import upload

    urls = upload("photo.jpg")

    print(urls[0])

─────────────────────────────────────────────
Quick Start (Async)
─────────────────────────────────────────────

    from meowbox import MeowBox

    mb = MeowBox()

    urls = await mb.upload_async("photo.jpg")

    print(urls[0])

─────────────────────────────────────────────
Features
─────────────────────────────────────────────

✓ Permanent file hosting
✓ Direct links
✓ Sync + async support
✓ Multiple file upload
✓ FastAPI compatible
✓ HTTPX async uploader
✓ Lightweight
✓ Telegram bot friendly
"""

__version__ = "2.4"

__author__ = "@BadmundaXd"

__repo__ = "https://github.com/Badmunda05/MeowBox"


# ─────────────────────────────────────────────
# Imports
# ─────────────────────────────────────────────

from .meowbox import (
    MeowBox,
    upload,
)

from .meowbox_async import (
    upload_async,
)

from .exceptions import (
    MeowBoxException,
    UploadError,
    RateLimitError,
    DeleteError,
)


# ─────────────────────────────────────────────
# Exports
# ─────────────────────────────────────────────

__all__ = [
    "MeowBox",
    "upload",
    "upload_async",
    "MeowBoxException",
    "UploadError",
    "RateLimitError",
    "DeleteError",
]
