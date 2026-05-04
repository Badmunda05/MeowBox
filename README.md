# MeowBox Python Library 📦

> **Permanent file hosting — files never expire.**
> By [@BadmundaXd](https://t.me/BadmundaXd) | [GitHub](https://github.com/Badmunda05/MeowBox)

Python library for uploading files to [MeowBox](https://files.tgvibes.online) — supports both sync and async.

---

## Install

```bash
pip install meowbox
```

---

## Quick Start

### Sync upload
```python
from meowbox import upload

urls = upload("photo.jpg")
print(urls[0])
# https://files.tgvibes.online/AbCdEfGh.jpg
```

### Async upload (httpx)
```python
from meowbox import upload_async

urls = await upload_async("photo.jpg")
print(urls[0])
```

### Class-based
```python
from meowbox import MeowBox

mb = MeowBox()

# Sync
urls = mb.upload("photo.jpg")

# Async
urls = await mb.upload_async("photo.jpg")
```

### Upload multiple files
```python
from meowbox import upload

urls = upload(["file1.jpg", "file2.mp4", "file3.pdf"])
for url in urls:
    print(url)
```

### Upload file object (e.g. Telegram Bot)
```python
from meowbox import upload_async

path = await message.download()
urls = await upload_async(path)
await message.reply(urls[0])
```

---

## Telegram Bot Example

```python
from meowbox import upload_async
import os

async def upload_handler(message):
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply("Reply to a file!")
        return

    path = await message.reply_to_message.download()
    try:
        urls = await upload_async(path)
        await message.reply(f"✅ {urls[0]}")
    except Exception as e:
        await message.reply(f"❌ Upload failed: {e}")
    finally:
        if os.path.exists(path):
            os.remove(path)
```

---

## Exceptions

| Exception | When |
|-----------|------|
| `UploadError` | Upload failed (server error) |
| `RateLimitError` | Too many uploads |
| `MeowBoxException` | Base exception |

```python
from meowbox import upload
from meowbox.exceptions import UploadError, RateLimitError

try:
    urls = upload("file.jpg")
except RateLimitError as e:
    print(f"Slow down! Retry after {e.retry_after}s")
except UploadError as e:
    print(f"Upload failed: {e}")
```

---

## API Reference

### `upload(f, base_url=...) -> list[str]`
Sync upload. `f` = path, file object, or list of either.

### `upload_async(f, base_url=...) -> list[str]`
Async upload using httpx.

### `MeowBox(base_url=...)`
Class with `.upload()` and `.upload_async()` methods.

---

## Links

- 🌐 Site: [files.tgvibes.online](https://files.tgvibes.online)
- 💬 Telegram: [@BadmundaXd](https://t.me/BadmundaXd)
- 📦 Repo: [github.com/Badmunda05/MeowBox](https://github.com/Badmunda05/MeowBox)
