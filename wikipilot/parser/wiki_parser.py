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
    def __init__(self):
        self.state_stack = [ParserState.TEXT]
        self.output = []
        self.buffer = []

    def push_state(self, state):
        self.state_stack.append(state)

    def pop_state(self):
        if len(self.state_stack) > 1:
            self.state_stack.pop()

    def current_state(self):
        return self.state_stack[-1]

    def parse(self, text):
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
        if not self.buffer:
            return
        state = self.current_state()
        content = "".join(self.buffer)
        self.output.append((state, content))
        self.buffer = []
