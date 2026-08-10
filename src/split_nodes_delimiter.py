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
