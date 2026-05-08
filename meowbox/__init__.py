# -*- coding: utf-8 -*-
"""
MeowBox — Permanent File Hosting Python Library
Repo   : https://github.com/Badmunda05/MeowBox
Author : @BadmundaXd

Quick start:
    from meowbox import upload
    urls = upload("photo.jpg")
    print(urls[0])

Async:
    from meowbox import MeowBox
    mb = MeowBox()
    urls = await mb.upload_async("photo.jpg")
"""

__version__ = "1.0.1"
__author__  = "@BadmundaXd"
__repo__    = "https://github.com/Badmunda05/MeowBox"

from .meowbox import MeowBox, upload
from .meowbox_async import upload_async
from .exceptions import MeowBoxException, UploadError, RateLimitError, DeleteError

__all__ = [
    "MeowBox",
    "upload",
    "upload_async",
    "MeowBoxException",
    "UploadError",
    "RateLimitError",
    "DeleteError",
]
