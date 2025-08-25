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
from wiki_token import WikiToken


class ParseResult:
    """
    A tree node representing a parsed segment.

    - state: the ParserState of this node
    - children: nested ParseResults or WikiTokens
    """
    def __init__(self, state: ParserState):
        self.state: ParserState = state
        self.children: typing.List[typing.Union['ParseResult', WikiToken]] = []

    def add_child(self, child: typing.Union['ParseResult', WikiToken]):
        self.children.append(child)

    def get_text(self) -> str:
        """Flatten all text in this subtree."""
        parts = []
        for child in self.children:
            if isinstance(child, WikiToken):
                parts.append(child.text)
            else:
                parts.append(child.get_text())
        return "".join(parts)

    def get_text_by_state(self, state: ParserState) -> str:
        """Return all text for nodes matching a specific state."""
        parts = []
        if self.state == state:
            parts.append(self.get_text())
        for child in self.children:
            if isinstance(child, ParseResult):
                parts.append(child.get_text_by_state(state))
        return "".join(parts)

    def __repr__(self):
        return f"ParseResult({self.state}, children={self.children!r})"
