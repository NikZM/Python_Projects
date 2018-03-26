import unittest
import sys
sys.path.append('./api/rest/')

import SampleHelper


class SampleHelperTest(unittest.TestCase):

    def test_process_returnsTAGC_WhenGiven_ATCG(self):
        inversed_sample = SampleHelper.process("ATCG", "1", "2000-01-01 00:00:00")['sequence']
        self.assertEqual(inversed_sample, 'TAGC')

    def test_process_returnsCGCGCGTTTAAAA_WhenGiven_GCGCGCAAATTTT(self):
        inversed_sample = SampleHelper.process("GCGCGCAAATTTT", "1", "2000-01-01 00:00:00")['sequence']
        self.assertEqual(inversed_sample, 'CGCGCGTTTAAAA')

    def test_generate_sequence_only_contains_ATCG(self):
        success = True
        for s in SampleHelper.generate()['sequence']:
            if s != "A" and s != "C" and s != "T" and s != "G":
                success = False

        self.assertTrue(success)

    def test_generate_sequence_is_between_1_and_100(self):
        length = len(SampleHelper.generate()['sequence'])
        self.assertTrue(length > 0 and length <= 100)


if __name__ == '__main__':
    unittest.main()
