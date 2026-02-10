import unittest
from analysis.mapping import map_columns, missing_required


class MappingTests(unittest.TestCase):
    def test_maps_common_aliases(self):
        headers = ['Therapeutic Tag', 'SKU', 'Revenue', 'ISSUE_QTY', 'CLOSING_QTY']
        mapping = map_columns(headers)
        self.assertEqual(mapping['category'], 'Therapeutic Tag')
        self.assertEqual(mapping['issue_qty'], 'ISSUE_QTY')
        self.assertEqual(missing_required(mapping), [])

    def test_missing_columns(self):
        mapping = map_columns(['foo', 'bar'])
        self.assertIn('revenue', missing_required(mapping))


if __name__ == '__main__':
    unittest.main()
