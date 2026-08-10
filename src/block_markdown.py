from enum import Enum

from extract_markdown import markdown_to_blocks
from htmlnode import HTMLNode, LeafNode, ParentNode
from split_nodes import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST

    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            paragraph_text = " ".join(lines)

            children = text_to_children(paragraph_text)

            node = ParentNode("p", children)
            children_nodes.append(node)
        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            new_lines = []
            for line in lines:
                new_lines.append(line.lstrip(">").strip())
            quote_text = " ".join(new_lines)

            children = text_to_children(quote_text)
            node = ParentNode("blockquote", children)
            children_nodes.append(node)
        elif block_type == BlockType.HEADING:
            parts = block.split(" ", 1)
            heading_text = parts[1].strip() if len(parts) > 1 else ""
            children = text_to_children(heading_text)
            node = ParentNode(f"h{len(parts[0])}", children)
            children_nodes.append(node)
        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            code_text = "\n".join(lines[1:-1]) + "\n"
            text_node = TextNode(code_text, TextType.TEXT)
            child_node = text_node_to_html_node(text_node)

            code_node = ParentNode("code", [child_node])

            pre_node = ParentNode("pre", [code_node])

            children_nodes.append(pre_node)
        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            childrens = []
            for line in lines:
                sections = line.split(" ", 1)
                children_node = ParentNode(
                    "li",
                    text_to_children(sections[1].strip() if len(sections) > 1 else ""),
                )
                childrens.append(children_node)

            node = ParentNode("ul", childrens)
            children_nodes.append(node)
        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            childrens = []
            for line in lines:
                sections = line.split(" ", 1)
                children_node = ParentNode(
                    "li",
                    text_to_children(sections[1].strip() if len(sections) > 1 else ""),
                )
                childrens.append(children_node)

            node = ParentNode("ol", childrens)
            children_nodes.append(node)
    div_parent_node = ParentNode("div", children_nodes)
    return div_parent_node


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for text_node in text_nodes:
        html_nodes.append(text_node_to_html_node(text_node))
    return html_nodes
