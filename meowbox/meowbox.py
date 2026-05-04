# -*- coding: utf-8 -*-
"""
MeowBox — Permanent File Hosting
Repo   : https://github.com/Badmunda05/MeowBox
Author : @BadmundaXd <munda.bad1322@gmail.com>
"""

import os
import requests
from .exceptions import MeowBoxException, UploadError, RateLimitError, DeleteError

MEOWBOX_URL = "https://files.tgvibes.online/upload"


# ─────────────────────────────────────────────
#  MeowBox Class (sync)
# ─────────────────────────────────────────────

class MeowBox:
    """
    MeowBox uploader — sync + async support.

    Usage (sync):
        from meowbox import MeowBox
        mb = MeowBox()
        urls = mb.upload("photo.jpg")
        print(urls[0])

    Usage (async):
        from meowbox import MeowBox
        mb = MeowBox()
        urls = await mb.upload_async("photo.jpg")
        print(urls[0])
    """

    def __init__(self, base_url: str = MEOWBOX_URL):
        self.base_url = base_url

    def upload(self, f) -> list:
        """Upload file(s) to MeowBox. Returns list of direct URLs."""
        return upload(f, base_url=self.base_url)

    async def upload_async(self, f) -> list:
        """Async upload file(s) to MeowBox. Returns list of direct URLs."""
        from .meowbox_async import upload_async
        return await upload_async(f, base_url=self.base_url)

    def __repr__(self):
        return f"MeowBox(url={self.base_url!r})"


# ─────────────────────────────────────────────
#  Sync functions
# ─────────────────────────────────────────────

def upload(f, base_url: str = MEOWBOX_URL) -> list:
    """
    Upload file(s) to MeowBox (sync).

    Args:
        f: File path (str), file object, or list of either.
        base_url: MeowBox upload endpoint.

    Returns:
        list of direct URLs (str).

    Raises:
        UploadError: If upload fails.
        RateLimitError: If rate limited.

    Example:
        from meowbox import upload
        urls = upload("photo.jpg")
        print(urls[0])  # https://files.tgvibes.online/AbCdEfGh.jpg
    """
    files_input = [f] if not isinstance(f, (list, tuple)) else list(f)
    urls = []

    for item in files_input:
        if isinstance(item, str):
            filename = os.path.basename(item)
            fobj = open(item, "rb")
            opened = True
        else:
            filename = getattr(item, "name", "upload")
            fobj = item
            opened = False

        try:
            resp = requests.post(
                base_url,
                files={"files[]": (filename, fobj)},
                timeout=120,
            )
        finally:
            if opened:
                fobj.close()

        if resp.status_code == 429:
            raise RateLimitError()

        try:
            data = resp.json()
        except Exception:
            raise UploadError(f"Invalid response (HTTP {resp.status_code}): {resp.text[:200]}")

        if not data.get("success"):
            raise UploadError(f"Upload failed: {data.get('description', 'Unknown error')}")

        for file_info in data.get("files", []):
            urls.append(file_info["url"])

    return urls
