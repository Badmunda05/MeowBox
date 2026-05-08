# -*- coding: utf-8 -*-
"""
MeowBox — Async uploader (httpx)
Repo   : https://github.com/Badmunda05/MeowBox
Author : @BadmundaXd <munda.bad1322@gmail.com>
"""

import os
from .exceptions import UploadError, RateLimitError

MEOWBOX_URL = "https://files.tgvibes.online/upload"


async def upload_async(f, base_url: str = MEOWBOX_URL) -> list:
    """
    Async upload file(s) to MeowBox using httpx.

    Args:
        f: File path (str), file object, or list of either.
        base_url: MeowBox upload endpoint.

    Returns:
        list of direct URLs (str).

    Raises:
        UploadError: If upload fails.
        RateLimitError: If rate limited.

    Example:
        from meowbox.meowbox_async import upload_async
        urls = await upload_async("photo.jpg")
        print(urls[0])  # https://files.tgvibes.online/AbCdEfGh.jpg
    """
    try:
        import httpx
    except ImportError:
        raise ImportError("httpx is required: pip install httpx")

    files_input = [f] if not isinstance(f, (list, tuple)) else list(f)
    urls = []

    async with httpx.AsyncClient(timeout=120) as client:
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
                resp = await client.post(
                    base_url,
                    files={"files[]": (filename, fobj)},
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
                           
