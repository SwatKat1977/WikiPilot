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
from parse_result import ParseResult
from pattern_rule import PatternRule
from wiki_token import WikiToken

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
        root = ParseResult(ParserState.TEXT)
        self.result_stack = [root]   # stack of ParseResult nodes
        self.buffer = []

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

    def current_result(self) -> ParseResult:
        return self.result_stack[-1]

    def parse(self, text) -> ParseResult:
        i = 0
        while i < len(text):
            matched = False
            for rule in self.rules:
                if rule.matches(text, i):
                    self.__flush_buffer()

                    # Closing state
                    if rule.exit_state and self.current_result().state == rule.exit_state:
                        finished = self.result_stack.pop()
                        self.current_result().add_child(finished)

                    # Opening state
                    elif rule.enter_state:
                        # Toggle same state
                        if self.current_result().state == rule.enter_state:
                            finished = self.result_stack.pop()
                            self.current_result().add_child(finished)
                        else:
                            new_node = ParseResult(rule.enter_state)
                            self.result_stack.append(new_node)

                    i += rule.length
                    matched = True
                    break

            if not matched:
                self.buffer.append(text[i])
                i += 1

        # Flush remaining buffer
        self.__flush_buffer()

        # Pop any remaining nodes and attach to root
        while len(self.result_stack) > 1:
            finished = self.result_stack.pop()
            self.result_stack[-1].add_child(finished)

        return self.result_stack[0]

    def __flush_buffer(self) -> None:
        """
        Flush the current buffer into the output list.

        Joins the buffered characters into a string and appends it to the output
        along with the current parser state. Clears the buffer afterward.
        """
        if not self.buffer:
            return

        text = "".join(self.buffer)
        self.current_result().add_child(WikiToken(ParserState.TEXT, text))
        self.buffer.clear()
