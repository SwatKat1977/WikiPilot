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
    """Holds the structured output of the parser as a list of Token objects."""

    def __init__(self, tokens: typing.List[WikiToken]):
        self.tokens = tokens

    def __iter__(self):
        return iter(self.tokens)

    def __len__(self):
        return len(self.tokens)

    def __getitem__(self, idx):
        return self.tokens[idx]

    def get_text(self) -> str:
        """Return the full plain text ignoring states."""
        return "".join(token.text for token in self.tokens)

    def get_text_by_state(self, state: ParserState) -> str:
        """Return concatenated text for a specific state."""
        return "".join(token.text for token in self.tokens if token.state == state)

    def __repr__(self):
        return f"<ParseResult tokens={self.tokens!r}>"
