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
import dataclasses
import typing
from parser_state import ParserState

@dataclasses.dataclass
class PatternRule:
    """
    Represents a token-matching rule for a parsing system.

    Each rule defines a fixed token string and the parser state transitions
    that should occur when the token is matched in the input text.

    Attributes:
        token (str): The literal string to match in the text.
        length (int): The length of the token. This should usually equal
            len(token), but can be stored explicitly for efficiency.
        enter_state (Optional[ParserState]): The parser state to transition
            into when this token is matched. Defaults to None.
        exit_state (Optional[ParserState]): The parser state to transition
            out of when this token is matched. Defaults to None.

    Methods:
        matches(text: str, index: int) -> bool:
            Check whether the token matches the given text starting at
            a specific index.
    """
    token: str
    length: int
    enter_state: typing.Optional[ParserState] = None
    exit_state: typing.Optional[ParserState] = None

    def matches(self, text: str, index: int) -> bool:
        """
        Check if this rule's token matches the given text starting at a
        specific index.

        Args:
            text (str): The input string to search.
            index (int): The position in the string where the match should
                         begin.

        Returns:
            bool: True if the token matches at the given index, False
                  otherwise.

        Notes:
            - If `index` is beyond the end of the text, the result will be
              False.
            - Matching is case-sensitive and requires an exact match of the
              token.
            - This method does not check whether the matched substring
              extends beyond the text length (handled safely by
              str.startswith()).
        """
        return text.startswith(self.token, index)
