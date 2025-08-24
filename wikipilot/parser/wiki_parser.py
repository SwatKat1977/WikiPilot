"""
This source file is part of WikiPilot
For the latest info, see https://github.com/SwatKat1977/WikiPilot

Copyright 2025 SwatKat1977

    This program is free software : you can redistribute it and /or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.If not, see < https://www.gnu.org/licenses/>.
"""
from parser_state import ParserState

BOLD_ITALIC_MARKDOWN: str = "'''''"
BOLD_MARKDOWN: str = "'''"
ITALIC_MARKDOWN: str = "''"
LINK_MARKDOWN_OPEN: str = "[["
LINK_MARKDOWN_CLOSE: str = "]]"
TEMPLATE_MARKDOWN_OPEN: str = "{{"
TEMPLATE_MARKDOWN_CLOSE: str = "}}"


class WikiParser:
    """
    A simple parser for processing Wiki-style markup into structured output.

    The parser recognizes formatting markers such as bold ('''), italics (''),
    bold+italic ('''''), links ([[...]]), and templates ({{...}}). Text is
    processed into segments, each tagged with its corresponding `ParserState`.

    Attributes:
        state_stack (list[ParserState]): A stack representing the current parsing states.
        output (list[tuple[ParserState, str]]): The parsed output as a list of (state, text) tuples.
        buffer (list[str]): A temporary buffer for accumulating characters before flushing them.
    """

    def __init__(self):
        """
        Initialize a new WikiParser instance.

        Starts with the parser in the `TEXT` state, with empty output and buffer.
        """
        self.state_stack = [ParserState.TEXT]
        self.output = []
        self.buffer = []
        self.rules = [
            # token, length, enter_state, exit_state
            (BOLD_ITALIC_MARKDOWN, 5, ParserState.BOLD_ITALIC, ParserState.BOLD_ITALIC),
            (BOLD_MARKDOWN, 3, ParserState.BOLD, ParserState.BOLD),
            (ITALIC_MARKDOWN, 2, ParserState.ITALIC, ParserState.ITALIC),

            (LINK_MARKDOWN_OPEN, 2, ParserState.LINK, None),
            (LINK_MARKDOWN_CLOSE, 2, None, ParserState.LINK),

            (TEMPLATE_MARKDOWN_OPEN, 2, ParserState.TEMPLATE, None),
            (TEMPLATE_MARKDOWN_CLOSE, 2, None, ParserState.TEMPLATE),
        ]

    def push_state(self, state):
        """
        Push a new parser state onto the state stack.

        Args:
            state (ParserState): The new parsing state to enter.
        """
        self.state_stack.append(state)

    def pop_state(self) -> None:
        """
        Pop the most recent parser state from the state stack.

        Ensures that at least one state (TEXT) remains on the stack.
        """
        if len(self.state_stack) > 1:
            self.state_stack.pop()

    def current_state(self) -> ParserState:
        """
        Get the current parsing state.

        Returns:
            ParserState: The parser state at the top of the stack.
        """
        return self.state_stack[-1]

    def parse(self, text: str):
        i: int = 0

        while i < len(text):
            matched: bool = False

            # Try each rule
            for token, length, *states in self.rules:
                if text.startswith(token, i):
                    self.flush_buffer()
                    enter_state = states[0] if len(states) > 0 else None
                    exit_state = states[1] if len(states) > 1 else None

                    # Toggle logic
                    if exit_state and self.current_state() == exit_state:
                        self.pop_state()

                    elif enter_state:
                        # If same state, pop; otherwise, push
                        if self.current_state() == enter_state:
                            self.pop_state()

                        else:
                            self.push_state(enter_state)

                    i += length
                    matched = True
                    break

            if not matched:
                # No rule matched, treat as normal text
                self.buffer.append(text[i])
                i += 1

        self.flush_buffer()
        return self.output

    def flush_buffer(self) -> None:
        """
        Flush the current buffer into the output list.

        Joins the buffered characters into a string and appends it to the output
        along with the current parser state. Clears the buffer afterward.
        """
        if not self.buffer:
            return
        state = self.current_state()
        content = "".join(self.buffer)
        self.output.append((state, content))
        self.buffer = []
