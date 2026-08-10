import unittest

from block_markdown import BlockType, block_to_block_type


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "> quote\n> line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "- item 1\n- item 2"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "This is a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
