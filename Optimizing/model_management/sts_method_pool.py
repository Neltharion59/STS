# Library-like script providing pool of all simple STS methods
import os
root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
import sys
sys.path.append(root_path)

from basic_similarity_methods.character_based import *
from basic_similarity_methods.statistical import *
from basic_similarity_methods.knowledge_based import wu_palmer_similarity_sentence, path_similarity_sentence, \
    leacock_chodorow_similarity_sentence, args_knowledge
from basic_similarity_methods.vector_based import *
from model_management.sts_method_wrappers import STSMethod


# Generates all combinations of parameters.
# Params: dict, dict
# Return: dict...
def all_arg_variations(arg_full_dict, output_arg_dict):

    # If we reached last param, let's yield the result
    if not bool(arg_full_dict):
        yield output_arg_dict

    # Loop over all params
    for parameter in arg_full_dict:
        # Loop over all values of current param
        for value in arg_full_dict[parameter]:
            # Add current value to current combination
            output_arg_dict_new = dict(output_arg_dict)
            output_arg_dict_new[parameter] = value

            # Jump to next param
            yield from all_arg_variations({i: arg_full_dict[i] for i in arg_full_dict if i != parameter}, output_arg_dict_new)
        break


# Adds method to method pool
# Params: str, dict, func<... -> float>, dict<str, STSMethod>
# Return:
def add_to_method_pool(method_name, method_arg_possibilites, method_function, method_pool):
    if len(list(all_arg_variations(method_arg_possibilites, {}))) == 1:
        sts_method = STSMethod(method_name, method_function, {})
        if method_name not in method_pool:
            method_pool[method_name] = []
        method_pool[method_name].append(sts_method)
    else:
        for arg_variation in list(all_arg_variations(method_arg_possibilites, {})):
            sts_method = STSMethod(method_name, method_function, arg_variation)
            if method_name not in method_pool:
                method_pool[method_name] = []
            method_pool[method_name].append(sts_method)


# Dict with all available simple STS methods
sts_method_pool = {}
# -----------------------------------------------------------------------------
# ---------------------------   STRING   --------------------------------------
# -----------------------------------------------------------------------------
string_based_name_list = []
character_based_name_list = []
term_based_name_list = []

# Add Hamming similarity
name = "hamming"
args_hamming = {
    "normalization_strategy": ["longer", "shorter", "both"]
}
add_to_method_pool(name, args_hamming, hamming, sts_method_pool)
string_based_name_list.append(name)
character_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add levenshtein similarity
name = "levenshtein"
args_levenshtein = {
}
add_to_method_pool(name, args_levenshtein, levenshtein, sts_method_pool)
string_based_name_list.append(name)
character_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add damerau_levenshtein similarity
name = "damerau_levenshtein"
args_damerau_levenshtein = {
}
add_to_method_pool(name, args_damerau_levenshtein, damerau_levenshtein, sts_method_pool)
string_based_name_list.append(name)
character_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add jaro similarity
name = "jaro"
args_jaro = {
}
add_to_method_pool(name, args_jaro, jaro, sts_method_pool)
string_based_name_list.append(name)
character_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add jaro_winkler similarity
name = "jaro_winkler"
args_jaro_winkler = {
}
add_to_method_pool(name, args_jaro_winkler, jaro_winkler, sts_method_pool)
string_based_name_list.append(name)
character_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add needleman_wunsch similarity
name = "needleman_wunsch"
args_needleman_wunsch = {
}
add_to_method_pool(name, args_needleman_wunsch, needleman_wunsch, sts_method_pool)
string_based_name_list.append(name)
character_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add smith_waterman similarity
name = "smith_waterman"
args_smith_waterman = {
}
add_to_method_pool(name, args_smith_waterman, smith_waterman, sts_method_pool)
string_based_name_list.append(name)
character_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add jaccard similarity
name = "jaccard"
add_to_method_pool(name, args_set_based, jaccard, sts_method_pool)
string_based_name_list.append(name)
term_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add sorensen_dice similarity
name = "sorensen_dice"
add_to_method_pool(name, args_set_based, sorensen_dice, sts_method_pool)
string_based_name_list.append(name)
term_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add overlap similarity
name = "overlap"
add_to_method_pool(name, args_set_based, overlap, sts_method_pool)
string_based_name_list.append(name)
term_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add cosine similarity
name = "cosine"
add_to_method_pool(name, {}, cosine, sts_method_pool)
string_based_name_list.append(name)
term_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add lcsseq similarity
name = "lcsseq"
add_to_method_pool(name, {}, lcsseq, sts_method_pool)
string_based_name_list.append(name)
character_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add lcsstr similarity
name = "lcsstr"
add_to_method_pool(name, {}, lcsstr, sts_method_pool)
string_based_name_list.append(name)
character_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add ochiai similarity
name = "ochiai"
add_to_method_pool(name, args_set_based, ochiai, sts_method_pool)
string_based_name_list.append(name)
term_based_name_list.append(name)
# -----------------------------------------------------------------------------
# ---------------------------   VECTOR   --------------------------------------
# -----------------------------------------------------------------------------
corpus_based_name_list = []

# Add hal similarity
name = "hal"
args_hal = {key: value for (key, value) in args_vector_based.items()}
args_hal['size'] = ['full', '200', '800']
add_to_method_pool(name, args_hal, hal, sts_method_pool)
corpus_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add lsa similarity
name = "lsa"
add_to_method_pool(name, args_vector_based, lsa, sts_method_pool)
corpus_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add esa similarity
name = "esa"
add_to_method_pool(name, args_vector_based, esa, sts_method_pool)
corpus_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add disco similarity
name = "disco"
args_disco = {key: value for (key, value) in args_vector_based.items()}
args_disco['version'] = ['raw', 'so_5', 'so_15']
add_to_method_pool(name, args_disco, disco, sts_method_pool)
corpus_based_name_list.append(name)
# Add openai similarity
name = "openai"
args_openai = {key: value for (key, value) in args_vector_based.items()}
args_openai['version'] = ['word_3-small', 'word_3-large', 'word_ada-002']
add_to_method_pool(name, args_openai, openai, sts_method_pool)
corpus_based_name_list.append(name)
# Add fast_text similarity
name = "fast_text"
add_to_method_pool(name, args_vector_based, fast_text, sts_method_pool)
corpus_based_name_list.append(name)
# Add PMI similarity
name = "pmi"
add_to_method_pool(name, args_pmi, pmi, sts_method_pool)
corpus_based_name_list.append(name)
# -----------------------------------------------------------------------------
# ------------------------   KNOWLEDGE   --------------------------------------
# -----------------------------------------------------------------------------
knowledge_based_name_list = []

# Add Wu-Palmer similarity
name = "wu_palmer"
add_to_method_pool(name, args_knowledge, wu_palmer_similarity_sentence, sts_method_pool)
knowledge_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add Path similarity
name = "path"
add_to_method_pool(name, args_knowledge, path_similarity_sentence, sts_method_pool)
knowledge_based_name_list.append(name)
# -----------------------------------------------------------------------------
# Add Leacock-Chodorow similarity
name = "leacock_chodorow"
add_to_method_pool(name, args_knowledge, leacock_chodorow_similarity_sentence, sts_method_pool)
knowledge_based_name_list.append(name)
# -----------------------------------------------------------------------------
