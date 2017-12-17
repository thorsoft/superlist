import unittest
from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # Edith goes to the homepage and accidentally tries to submit an
        # empty  list item. She hits Enter on the empty inputbox

        # The home page refreshes and there is an error message saying
        # that empty list items cannot be blank

        # she tries again with some text for the item, which now works.

        # Perversely she now decides to submit a second blank list item
        # She receives a similar warning on the list page.

        # And she can correct by filling in some text.
        self.fail("write me")



if __name__ == '__main__':
    unittest.main(warnings='ignore')
