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
import enum


class ParserState(enum.Enum):
    """
    Enumeration representing the different parsing states for text processing.
    These states are typically used in a parser to determine how to interpret
    and format portions of text.
    """

    BOLD = enum.auto()
    """State indicating that the parser is currently processing bold text."""

    BOLD_ITALIC = enum.auto()
    """State indicating that the parser is currently processing text that is
       both bold and italic."""

    ITALIC = enum.auto()
    """State indicating that the parser is currently processing italic text."""

    LINK = enum.auto()
    """State indicating that the parser is currently processing a hyperlink."""

    TEMPLATE = enum.auto()
    """State indicating that the parser is currently processing a template or
       placeholder structure."""

    TEXT = enum.auto()
    """Default state indicating that the parser is processing plain text."""
