import unittest
import SequenceAlignment
import BioPythonTest
import random

def random_string(length):
    return ''.join(random.choice('ACTG') for _ in range(length))

#Actual output should be same as at least one of the expected outputs
def is_aligned(actual_output, expected_output):
    for alignment in expected_output:
        output_seq1 = alignment[0].replace('-','_')
        output_seq2 = alignment[1].replace('-','_')
        if output_seq1 == actual_output[0] and output_seq2 == actual_output[1]:
            return True
            break
    print('Failure :: :: :: ')
    print(f'Actual output :: {actual_output}')
    print(f'Expected Output :: {expected_output}')
    return False

def is_optimum_score(actual_output, expected_output):
    actual_score = SequenceAlignment.getScore(actual_output[0], actual_output[1])
    for alignment in expected_output:
        output_seq1 = alignment[0].replace('-','_')
        output_seq2 = alignment[1].replace('-','_')
        expected_score = SequenceAlignment.getScore(output_seq1, output_seq2)
        if expected_score == actual_score:
            return True
            break
    print('Failure :: :: :: ')
    print(f'Actual score :: {actual_score}')
    print(f'Expected score :: {expected_score}')
    return False

class TestAlignment(unittest.TestCase):

    def test1(self):
        str1 = random_string(1)
        str2 = random_string(1)
        actual_output = SequenceAlignment.sequenceAlignment(str1,str2)
        expected_output = BioPythonTest.get_alignment(str1, str2)
        self.assertTrue(is_aligned(actual_output, expected_output))

    def test2(self):
        str1 = random_string(15)
        str2 = random_string(15)
        actual_output = SequenceAlignment.sequenceAlignment(str1,str2)
        expected_output = BioPythonTest.get_alignment(str1, str2)
        self.assertTrue(is_aligned(actual_output, expected_output))

    def test3(self):
        str1 = random_string(110)
        str2 = random_string(1000)
        actual_output = SequenceAlignment.sequenceAlignment(str1,str2)
        expected_output = BioPythonTest.get_alignment(str1, str2)
        self.assertTrue(is_optimum_score(actual_output, expected_output))

if __name__ == '__main__':
    unittest.main()
