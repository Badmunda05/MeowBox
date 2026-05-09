# -*- coding: utf-8 -*-
"""
MeowBox — Permanent File Hosting
Repo   : https://github.com/Badmunda05/MeowBox
Author : @BadmundaXd <munda.bad1322@gmail.com>
"""

import os
import requests
from .exceptions import (
    MeowBoxException,
    UploadError,
    RateLimitError,
    DeleteError,
)

MEOWBOX_URL = "https://files.tgvibes.online/upload"


# ─────────────────────────────────────────────
#  MeowBox Class (sync + async)
# ─────────────────────────────────────────────

class MeowBox:
    """
    Usage:

        from meowbox import MeowBox

        mb = MeowBox()

        urls = mb.upload("photo.jpg")
        print(urls[0])

    Async:

        urls = await mb.upload_async("photo.jpg")
        print(urls[0])
    """

    def __init__(self, base_url: str = MEOWBOX_URL):
        self.base_url = base_url

    def upload(self, f) -> list:
        return upload(f, base_url=self.base_url)

    async def upload_async(self, f) -> list:
        from .meowbox_async import upload_async
        return await upload_async(f, base_url=self.base_url)

    def __repr__(self):
        return f"MeowBox(url={self.base_url!r})"


# ─────────────────────────────────────────────
#  Sync Upload
# ─────────────────────────────────────────────

def upload(f, base_url: str = MEOWBOX_URL) -> list:
    """
    Upload file(s) to MeowBox.

    Supports:
    - file path
    - file object
    - list of files

    Returns:
        list[str]
    """

    files_input = [f] if not isinstance(f, (list, tuple)) else list(f)

    urls = []

    for item in files_input:

        # ─── Open file ───────────────────────
        if isinstance(item, str):
            filename = os.path.basename(item)
            fobj = open(item, "rb")
            opened = True
        else:
            filename = getattr(item, "name", "upload")
            fobj = item
            opened = False

        try:

            # ─── Upload request ──────────────
            resp = requests.post(
                base_url,

                # FIXED FIELD NAME
                files={
                    "files": (filename, fobj)
                },

                # optional form data
                data={
                    "expiry": "never"
                },

                timeout=300,
            )

        finally:
            if opened:
                fobj.close()

        # ─── Rate limit ─────────────────────
        if resp.status_code == 429:
            raise RateLimitError()

        # ─── Invalid response ───────────────
        try:
            data = resp.json()
        except Exception:
            raise UploadError(
                f"Invalid response (HTTP {resp.status_code}): "
                f"{resp.text[:300]}"
            )

        # ─── Upload failed ──────────────────
        if not data.get("success"):
            raise UploadError(
                data.get("description")
                or data.get("message")
                or "Unknown upload error"
            )

        # ─── Extract URLs ───────────────────
        files_data = data.get("files", [])

        if not files_data:
            raise UploadError("No files returned from server")

        for file_info in files_data:

            # supports multiple response styles
            url = (
                file_info.get("url")
                or file_info.get("link")
                or file_info.get("src")
            )

            if not url:
                continue

            urls.append(url)

    if not urls:
        raise UploadError("Upload succeeded but no URL returned")

    return urls
