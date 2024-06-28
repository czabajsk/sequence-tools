"""
The Needleman-Wunsch Algorithm tests
"""

from unittest import TestCase

from needleman_wunsch import needleman_wunsch


class TestNeedlemanWunsch(TestCase):
    """
    Tests for the methods related to smple implementation
    of the Needleman Wunsch algorithm
    """

    def test_needleman_wunsch_simple(self):
        """
        Testing simple alignment
        """
        # given
        x = "GATTACA"
        y = "GCATGCU"
        # when
        result = needleman_wunsch(x, y)
        # then
        self.assertEqual("G-ATTACA\nGCA-TGCU", result)

    def test_needlman_wunsch_complex_gap_0(self):
        """
        Testing gap 0
        """
        # given
        x = "GCAGGCAAGTGGGGCACCCGTATCCTTTCCAACTTACAAGGGTCCCCGTT"
        y = "GTGCGCCAGAGGAAGTCACTTTATATCCGCGCACGGTACTCCTTTTTCTA"
        # when
        result = needleman_wunsch(x, y, gap=0)
        # then
        expected = (
            "----G-C--AGGCAAGTGGGGCACCCGTATCCT-T-T-C-C-AACTTACAAGGGT-C-CC-----CGT-T\n"
            "GTGCGCCAGAGG-AAGT----CA--C-T-T--TATATCCGCG--C--AC---GGTACTCCTTTTTC-TA-"
        )
        self.assertEqual(expected, result)

    def test_needlman_wunsch_complex_gap_1(self):
        """
        Testing gap 1
        """
        # given
        x = "GCAGGCAAGTGGGGCACCCGTATCCTTTCCAACTTACAAGGGTCCCCGTT"
        y = "GTGCGCCAGAGGAAGTCACTTTATATCCGCGCACGGTACTCCTTTTTCTA"
        # when
        result = needleman_wunsch(x, y, gap=1)
        # then
        expected = (
            "GCAG-GCAAGTGG--GGCAC-CCGTATCCTTTC-CAAC-TTACAAGGGTCC-CCGT-T-\n"
            "G-TGCGCCAGAGGAAGTCACTTTATATCC--GCGC-ACGGTAC-----TCCTTTTTCTA"
        )
        self.assertEqual(expected, result)

    def test_needlman_wunsch_complex_gap_2(self):
        """
        Testing gap 2
        """
        # given
        x = "GCAGGCAAGTGGGGCACCCGTATCCTTTCCAACTTACAAGGGTCCCCGTT"
        y = "GTGCGCCAGAGGAAGTCACTTTATATCCGCGCACGGTACTCCTTTTTCTA"
        # when
        result = needleman_wunsch(x, y, gap=2)
        # then
        expected = (
            "GCAGGCAAGTGG--GGCAC-CCGTATCCTTTCCAACTTACAAGGGTCCCCGTT\n"
            "GTGCGCCAGAGGAAGTCACTTTATATCC-GCGCACGGTAC-TCCTTTTTC-TA"
        )
        self.assertEqual(expected, result)
