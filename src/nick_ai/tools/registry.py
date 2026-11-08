from __future__ import annotations

from datetime import datetime


class ToolRegistry:
    """Explicit allow-list of safe, user-invoked tools."""

    def execute_command(self, text: str) -> str | None:
        command = text.strip()
        if command == "/help":
            return "دستورهای آماده: /help ، /time ، /calc 12*(3+4)"
        if command == "/time":
            return datetime.now().astimezone().strftime("زمان محلی سرور: %Y-%m-%d %H:%M:%S %Z")
        if command.startswith("/calc "):
            from .calculator import calculate
            try:
                return calculate(command[6:])
            except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as exc:
                return f"خطای محاسبه: {exc}"
        return None
