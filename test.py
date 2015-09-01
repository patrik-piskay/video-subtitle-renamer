import unittest
from movieSubtitleRenamer import extractCleanNameWithExtension

class TestRenamer(unittest.TestCase):

    def test_extracting_clean_name(self):
        testCases = [
            {
                'input': 'Mr.Robot.S04E03(3242342442222).srt',
                'output': ['Mr.Robot.S04E03', 'srt']
            },
            {
                'input': 'Mr.Robot.S04E03.HDTV.x264-KILLERS(3242342442222).srt',
                'output': ['Mr.Robot.S04E03', 'srt']
            },
            {
                'input': 'Mr.Robot.S04E03.HDTV.x264-KILLERS.srt',
                'output': ['Mr.Robot.S04E03', 'srt']
            },
            {
                'input': 'Some-Movie-2015.HDTV.x264.sub',
                'output': ['Some-Movie-2015', 'sub']
            },
            # TODO add more test cases
        ]

        for testCase in testCases:
            self.assertEqual(extractCleanNameWithExtension(testCase['input']), testCase['output'])

if __name__ == '__main__':
    unittest.main()