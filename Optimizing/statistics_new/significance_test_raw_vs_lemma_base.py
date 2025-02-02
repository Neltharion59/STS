import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from scipy.stats import shapiro, normaltest, ttest_ind, mannwhitneyu


def test_normality(sample, p_value):
    if 3 <= len(sample) <= 50:
        return 'shapiro', shapiro(sample).pvalue > p_value
    else:
        return 'dagostino', normaltest(sample).pvalue > p_value


def test_right_higher(l_sample, r_sample, is_normal, p_value):
    if is_normal:
        return 'student ttest', ttest_ind(l_sample, r_sample, alternative='less').pvalue > p_value
    else:
        return 'wilcox', mannwhitneyu(l_sample, r_sample, alternative='less').pvalue > p_value


def test_significance(left_sample, right_sample, p_value=0.05):
    if len(left_sample) != len(right_sample):
        raise ValueError('Samples need to be of equal size')

    if len(left_sample) < 3:
        raise ValueError('Samples must have at least 3 values')

    result = {
        'left': {},
        'right': {}
    }

    result['left']['normality_test'], result['left']['is_normal'] = test_normality(left_sample, p_value)
    result['right']['normality_test'], result['right']['is_normal'] = test_normality(right_sample, p_value)

    is_normal = result['left']['is_normal'] and result['right']['is_normal']

    result['right_higher_test'], result['right_higher'] = test_right_higher(left_sample, right_sample, is_normal, p_value)

    result['left']['is_normal'] = 1 if result['left']['is_normal'] else 0
    result['right']['is_normal'] = 1 if result['right']['is_normal'] else 0
    result['right_higher'] = 1 if result['right_higher'] else 0

    return result
