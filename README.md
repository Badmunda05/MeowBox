# meowbox

> permanent file hosting — files never expire.
> by [badmunda](https://t.me/BadmundaXd) · [github](https://github.com/Badmunda05/MeowBox)

a python library for uploading files to [meowbox](https://files.tgvibes.online).
supports both sync and async out of the box.

---

## install

```bash
pip install meowbox
```

---

## how to use

### basic sync upload

```python
from meowbox import upload

urls = upload("photo.jpg")
print(urls[0])
# https://files.tgvibes.online/AbCdEfGh.jpg
```

### async upload

```python
from meowbox import upload_async

urls = await upload_async("photo.jpg")
print(urls[0])
```

### class-based usage

```python
from meowbox import MeowBox

mb = MeowBox()

# sync
urls = mb.upload("photo.jpg")

# async
urls = await mb.upload_async("photo.jpg")
```

### upload multiple files

```python
from meowbox import upload

urls = upload(["file1.jpg", "file2.mp4", "file3.pdf"])
for url in urls:
    print(url)
```

### upload from a file object

```python
from meowbox import upload_async

path = await message.download()
urls = await upload_async(path)
await message.reply(urls[0])
```

---

## telegram bot example

```python
from meowbox import upload_async
import os

async def upload_handler(message):
    if not message.reply_to_message or not message.reply_to_message.media:
        await message.reply("reply to a file!")
        return

    path = await message.reply_to_message.download()
    try:
        urls = await upload_async(path)
        await message.reply(f"✅ {urls[0]}")
    except Exception as e:
        await message.reply(f"❌ upload failed: {e}")
    finally:
        if os.path.exists(path):
            os.remove(path)
```

---

## error handling

| exception | when |
|-----------|------|
| `UploadError` | upload failed (server error) |
| `RateLimitError` | too many requests |
| `MeowBoxException` | base exception class |

```python
from meowbox import upload
from meowbox.exceptions import UploadError, RateLimitError

try:
    urls = upload("file.jpg")
except RateLimitError as e:
    print(f"slow down! retry after {e.retry_after}s")
except UploadError as e:
    print(f"upload failed: {e}")
```

---

## api reference

| method | description |
|--------|-------------|
| `upload(f, base_url=...)` | sync upload — accepts path, file object, or list |
| `upload_async(f, base_url=...)` | async upload using httpx |
| `MeowBox(base_url=...)` | class with `.upload()` and `.upload_async()` methods |

---

## links

[![telegram](https://img.shields.io/badge/telegram-group-white?style=social&logo=telegram)](https://t.me/PBXCHATS)
[![channel](https://img.shields.io/badge/telegram-channel-white?style=social&logo=telegram)](https://t.me/PBX_UPDATE)
