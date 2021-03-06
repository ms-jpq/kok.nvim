from asyncio import Future, Queue
from itertools import count
from typing import Awaitable, Callable, Tuple


def schedule(
    chan: Queue,
) -> Tuple[Callable[[], Awaitable[None]], Callable[[], Tuple[int, Future]]]:
    it = count()
    uid = next(it)
    fut: Future = Future()

    async def background_update() -> None:
        while True:
            rid, resp = await chan.get()
            if rid >= uid and not fut.done():
                fut.set_result(resp)

    def require() -> Tuple[int, Future]:
        nonlocal uid, fut
        uid = next(it)
        fut.cancel()
        fut = Future()
        return uid, fut

    return background_update, require
