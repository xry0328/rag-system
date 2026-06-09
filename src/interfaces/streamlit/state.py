from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterator


def consume_async_iterator(iterator: AsyncIterator) -> Iterator:
    loop = asyncio.new_event_loop()
    try:
        while True:
            try:
                yield loop.run_until_complete(iterator.__anext__())
            except StopAsyncIteration:
                break
    finally:
        loop.close()

