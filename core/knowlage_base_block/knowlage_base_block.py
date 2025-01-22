"""
KBBlock using mistletoe for AST parsing
"""

import pathlib
from dataclasses import dataclass, field

from mistletoe import Document  # type: ignore
from mistletoe.block_token import BlockToken, Heading, SetextHeading, BlockCode, CodeFence, List, ListItem, Table, TableRow, TableCell  # type: ignore
from mistletoe.token import Token  # type: ignore
from mistletoe.span_token import SpanToken  # type: ignore
from mistletoe.ast_renderer import AstRenderer  # type: ignore
from mistletoe.base_renderer import BaseRenderer  # type: ignore
from typing import Any

__all__ = [
    'KnowlageBaseBlock',
    'KnowlageBaseBlockFactory'
    ]

MdContext = dict[str, Any]


@dataclass
class KnowlageBaseBlock:
    body: str
    md_context: MdContext = field(default_factory=dict)
    childrens: list["KnowlageBaseBlock"] = field(default_factory=list)


def parse_token_block(token: BlockToken) -> tuple[str, list[BlockToken], MdContext]:
    ctx: MdContext = {}
    childs: list[BlockToken] = []
    body: str = ''
    render: BaseRenderer = AstRenderer()
    with render as renderer:
        body = renderer.render(token)  # type: ignore

    ctx['type'] = type(token).__name__
    if isinstance(token, Document):
        ctx['footnotes'] = token.footnotes
    elif isinstance(token, Heading) or isinstance(token, SetextHeading):
        ctx['level'] = token.level
    elif isinstance(token, BlockCode) or isinstance(token, CodeFence):
        ctx['lang'] = token.language
    elif isinstance(token, List):
        ctx['loose'] = token.loose
        ctx['start'] = token.start
    elif isinstance(token, ListItem):
        ctx['indentation'] = token.indentation
        ctx['loose'] = token.loose
        ctx['leader'] = token.leader
        ctx['prepend'] = token.prepend
    elif isinstance(token, Table):
        ctx['header'] = token.header
        ctx['align'] = token.column_align
    elif isinstance(token, TableRow):
        ctx['align'] = token.row_align
    elif isinstance(token, TableCell):
        ctx['align'] = token.align

    if hasattr(token, "children") and token.children is not None:
        for child in token.children:  # type: ignore
            child: Token = child
            if isinstance(child, BlockToken):
                childs.append(child)
            elif isinstance(child, SpanToken):
                pass  # TODO: handle span token (а нужно ли?..)

    return body, childs, ctx


class KnowlageBaseBlockFactory:
    @staticmethod
    def _parse_block(block: BlockToken) -> KnowlageBaseBlock:
        body, childs, ctx = parse_token_block(block)
        kb_childs: list[KnowlageBaseBlock] = []
        for child in childs:
            kb_childs.append(KnowlageBaseBlockFactory._parse_block(child))
        kb_block = KnowlageBaseBlock(body, ctx, kb_childs)
        return kb_block

    @staticmethod
    def _parse_str(content: str) -> KnowlageBaseBlock:
        return KnowlageBaseBlockFactory._parse_block(Document(content))

    @staticmethod
    def _parse_file(file_path: pathlib.Path) -> KnowlageBaseBlock:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return KnowlageBaseBlockFactory._parse_str(content)

    @staticmethod
    def create_block_from_file_path(file_path: pathlib.Path) -> KnowlageBaseBlock:
        return KnowlageBaseBlockFactory._parse_file(file_path)