import unittest

from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_good_formatting(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_bad_formatting(self):
        md = """
      This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line      




  - This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        for start in ["# ", "## ", "### ", "#### ", "##### ", "###### "]:
            block = start + "Heading"
            self.assertEqual(BlockType.HEADING, block_to_block_type(block))

        self.assertNotEqual(BlockType.HEADING, "#Heading")
        self.assertNotEqual(BlockType.HEADING, "Heading")
        self.assertNotEqual(BlockType.HEADING, "#a#Heading")

    def test_code(self):
        block = "``` this is some code ```"
        self.assertEqual(BlockType.CODE, block_to_block_type(block))

        block = "`` this is not some code ```"
        self.assertNotEqual(BlockType.CODE, block_to_block_type(block))

    def test_quote(self):
        block = ">Quote 1.\n>Quote 2.\n>Quote 3."
        self.assertEqual(BlockType.QUOTE, block_to_block_type(block))

        block = ">Quote 1\n<Quote 2"
        self.assertNotEqual(BlockType.QUOTE, block_to_block_type(block))

    def test_unordered_list(self):
        block = "- Point A\n- Point B\n- Point C"
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

        block = "-Point A\n- Point B"
        self.assertNotEqual(BlockType.UNORDERED_LIST, block_to_block_type(block))

    def test_ordered_list(self):
        block = "1. first\n2. second\n3. thrid"
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

        block = "1. first\n3. third\n2. second"
        self.assertNotEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

        block = "1.first\n2. second\n3. third"
        self.assertNotEqual(BlockType.ORDERED_LIST, block_to_block_type(block))

    def tets_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(block))
