from extract_markdown import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for current_node in old_nodes:
        if current_node.text_type != TextType.TEXT:
            new_nodes.append(current_node)
            continue
        split_nodes = []
        nodes = current_node.text.split(delimiter)
        if len(nodes) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(nodes)):
            if nodes[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(nodes[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(nodes[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        images = extract_markdown_images(original_text)
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)

        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def text_to_textnodes(text):
    list_node = []
    list_node = split_nodes_delimiter(
        [TextNode(text, TextType.TEXT)], "**", TextType.BOLD
    )
    list_node = split_nodes_delimiter(list_node, "_", TextType.ITALIC)
    list_node = split_nodes_delimiter(list_node, "`", TextType.CODE)
    list_node = split_nodes_image(list_node)
    list_node = split_nodes_link(list_node)
