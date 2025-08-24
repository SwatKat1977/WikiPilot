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
import typing

from parser_state import ParserState
from pattern_rule import PatternRule

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
        self.output: list = []
        self.buffer: list = []

        self.rules = [
            # Toggle states (enter_state == exit_state)
            PatternRule(BOLD_ITALIC_MARKDOWN,
                        5,
                        enter_state=ParserState.BOLD_ITALIC,
                        exit_state=ParserState.BOLD_ITALIC),
            PatternRule(BOLD_MARKDOWN,
                        3,
                        enter_state=ParserState.BOLD,
                        exit_state=ParserState.BOLD),
            PatternRule(ITALIC_MARKDOWN,
                        2,
                        enter_state=ParserState.ITALIC,
                        exit_state=ParserState.ITALIC),

            # Link (open/close pair)
            PatternRule(LINK_MARKDOWN_OPEN,
                        2,
                        enter_state=ParserState.LINK),
            PatternRule(LINK_MARKDOWN_CLOSE,
                        2,
                        exit_state=ParserState.LINK),

            # Template (open/close pair)
            PatternRule(TEMPLATE_MARKDOWN_OPEN,
                        2,
                        enter_state=ParserState.TEMPLATE),
            PatternRule(TEMPLATE_MARKDOWN_CLOSE,
                        2,
                        exit_state=ParserState.TEMPLATE),
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

    def parse(self, text) -> list:
        """
        Parse the given input text using the defined pattern-matching rules.

        This method scans through the text character by character, attempting
        to match tokens defined in `self.rules`. When a rule matches, it may
        trigger state transitions (entering or exiting parser states) and
        flush any accumulated buffer content to the output.

        Args:
            text (str): The input string to parse.

        Returns:
            Any: The final parsed output, as stored in `self.output`.

        Parsing Logic:
            - Iterates through the text from left to right.
            - At each position:
                * If a rule matches:
                    - Flushes the buffer.
                    - If the rule specifies an `exit_state` matching the
                      current state, the parser pops that state (closing
                      token).
                    - If the rule specifies an `enter_state`, the parser
                      either pushes or toggles that state (opening token).
                    - Advances the index by the rule's token length.
                * If no rule matches:
                    - Appends the current character to the buffer.
                    - Advances the index by one.
            - After processing the text, flushes any remaining buffer content.

        Notes:
            - Matching is case-sensitive and performed using the rules'
              `PatternRule.matches()` method.
            - State management depends on helper methods:
              `current_state()`, `push_state()`, `pop_state()`, and
              `flush_buffer()`.
        """
        i: int = 0

        while i < len(text):
            matched = False

            for rule in self.rules:
                if rule.matches(text, i):
                    self.flush_buffer()

                    if rule.exit_state and self.current_state() == \
                       rule.exit_state:
                        # Closing token
                        self.pop_state()

                    elif rule.enter_state:
                        # Opening or toggle token
                        if self.current_state() == rule.enter_state:
                            self.pop_state()

                        else:
                            self.push_state(rule.enter_state)

                    i += rule.length
                    matched = True
                    break

            if not matched:
                # Regular text
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
