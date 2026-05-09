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

    Supports:
    - file path
    - file object
    - multiple files

    Returns:
        list[str]
    """

    try:
        import httpx
    except ImportError:
        raise ImportError("httpx is required: pip install httpx")

    files_input = [f] if not isinstance(f, (list, tuple)) else list(f)

    urls = []

    async with httpx.AsyncClient(timeout=300) as client:

        for item in files_input:

            # ─── Open file ───────────────────
            if isinstance(item, str):
                filename = os.path.basename(item)
                fobj = open(item, "rb")
                opened = True
            else:
                filename = getattr(item, "name", "upload")
                fobj = item
                opened = False

            try:

                # ─── Upload request ──────────
                resp = await client.post(
                    base_url,

                    # FIXED FIELD NAME
                    files={
                        "files": (filename, fobj)
                    },

                    # optional form data
                    data={
                        "expiry": "never"
                    },
                )

            finally:
                if opened:
                    fobj.close()

            # ─── Rate limit ─────────────────
            if resp.status_code == 429:
                raise RateLimitError()

            # ─── Parse response ─────────────
            try:
                data = resp.json()
            except Exception:
                raise UploadError(
                    f"Invalid response (HTTP {resp.status_code}): "
                    f"{resp.text[:300]}"
                )

            # ─── Upload failed ──────────────
            if not data.get("success"):
                raise UploadError(
                    data.get("description")
                    or data.get("message")
                    or "Unknown upload error"
                )

            # ─── Extract URLs ───────────────
            files_data = data.get("files", [])

            if not files_data:
                raise UploadError("No files returned from server")

            for file_info in files_data:

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
