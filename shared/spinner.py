"""Async spinner for long-running agent calls.

Usage:
    from shared.spinner import run_with_spinner

    response = await run_with_spinner(agent.run("Hello"), message="Sentry processing")
"""

from __future__ import annotations

import asyncio
import sys
from typing import Any, Coroutine


# ANSI escape codes for themed output
_CYAN = "\033[36m"
_YELLOW = "\033[33m"
_GREEN = "\033[32m"
_RESET = "\033[0m"
_CLEAR_LINE = "\r\033[K"

# Spinner frames — a circuit-board style animation
_FRAMES = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]


async def run_with_spinner(
    coro: Coroutine[Any, Any, Any],
    *,
    message: str = "Processing",
) -> Any:
    """Run an awaitable while showing an animated spinner on stderr.

    Args:
        coro: The coroutine to await (e.g. ``agent.run(prompt)``).
        message: Text shown next to the spinner.

    Returns:
        The result of the coroutine.
    """
    done = False
    elapsed = 0.0
    interval = 0.1

    async def _spin() -> None:
        nonlocal elapsed
        idx = 0
        while not done:
            frame = _FRAMES[idx % len(_FRAMES)]
            secs = f"{elapsed:.1f}s"
            sys.stderr.write(f"{_CLEAR_LINE}{_CYAN}{frame} {_YELLOW}{message}... {_RESET}({secs})")
            sys.stderr.flush()
            await asyncio.sleep(interval)
            elapsed += interval
            idx += 1

    spinner_task = asyncio.create_task(_spin())
    try:
        result = await coro
    finally:
        done = True
        await spinner_task
        secs = f"{elapsed:.1f}s"
        sys.stderr.write(f"{_CLEAR_LINE}{_GREEN}✔ {message} {_RESET}({secs})\n")
        sys.stderr.flush()

    return result
