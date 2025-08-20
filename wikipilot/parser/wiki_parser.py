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

    def push_state(self, state):
        """
        Push a new parser state onto the state stack.

        Args:
            state (ParserState): The new parsing state to enter.
        """
        self.state_stack.append(state)

    def pop_state(self):
        """
        Pop the most recent parser state from the state stack.

        Ensures that at least one state (TEXT) remains on the stack.
        """
        if len(self.state_stack) > 1:
            self.state_stack.pop()

    def current_state(self):
        """
        Get the current parsing state.

        Returns:
            ParserState: The parser state at the top of the stack.
        """
        return self.state_stack[-1]

    def parse(self, text):
        """
        Parse a string of Wiki-style text into structured output.

        Recognized markup includes:
            - ''''' (bold+italic toggle)
            - '''   (bold toggle)
            - ''    (italic toggle)
            - [[ ]] (link toggle)
            - {{ }} (template toggle)

        Text outside markup is treated as plain text.

        Args:
            text (str): The input text to parse.

        Returns:
            list[tuple[ParserState, str]]: A list of (state, text) tuples,
            where `state` indicates the formatting applied to `text`.
        """
        i = 0
        while i < len(text):
            ch = text[i]
            state = self.current_state()

            # Handle bold+italic
            if text[i:i+5] == "'''''":
                if state == ParserState.BOLD_ITALIC:
                    self.flush_buffer()
                    self.pop_state()
                else:
                    self.flush_buffer()
                    self.push_state(ParserState.BOLD_ITALIC)
                i += 5
                continue

            # Handle bold
            elif text[i:i+3] == "'''":
                if state == ParserState.BOLD:
                    self.flush_buffer()
                    self.pop_state()
                else:
                    self.flush_buffer()
                    self.push_state(ParserState .BOLD)
                i += 3
                continue

            # Handle italics
            elif text[i:i+2] == "''":
                if state == ParserState.ITALIC:
                    self.flush_buffer()
                    self.pop_state()
                else:
                    self.flush_buffer()
                    self.push_state(ParserState.ITALIC)
                i += 2
                continue

            # Handle links
            elif text[i:i+2] == "[[":
                self.flush_buffer()
                self.push_state(ParserState.LINK)
                i += 2
                continue
            elif text[i:i+2] == "]]" and state == ParserState.LINK:
                self.flush_buffer()
                self.pop_state()
                i += 2
                continue

            # Handle templates
            elif text[i:i+2] == "{{":
                self.flush_buffer()
                self.push_state(ParserState.TEMPLATE)
                i += 2
                continue
            elif text[i:i+2] == "}}" and state == ParserState.TEMPLATE:
                self.flush_buffer()
                self.pop_state()
                i += 2
                continue

            # Regular text
            else:
                self.buffer.append(ch)
                i += 1

        self.flush_buffer()
        return self.output

    def flush_buffer(self):
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
