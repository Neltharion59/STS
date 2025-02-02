import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from model_management.sts_method_pool import character_based_name_list
from statistics_new.plot_SIMPLE_base import get_values, print_values, test_lemma_significance


results = get_values(character_based_name_list)
print_values(results)
test_lemma_significance(results)
