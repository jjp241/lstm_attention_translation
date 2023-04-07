import math

source_sentence = 'so this means a strict subset'
reference_translations = [
    'czyli to oznacza podzbiór właściwy',
    # 'w takim razie to oznacza podzbiór właściwy'
]

nmt_translations = [
    'czyli to podzbiór właściwy',
    'w takim razie to oznacza jest zbiór właściwy'
]

def get_ngrams_occurrences(n: int, text: str) -> dict[str, int]:
    """
    Returns a dict: ngram to number of occurrences
    """
    text = text.split(' ')
    ngrams = {}
    for i in range(len(text) - n + 1):
        ngram = " ".join(text[i:i+n])
        ngrams[ngram] = ngrams.get(ngram, 0) + 1
    return ngrams


def calc_p(n: int, references, candidate):
    """
    Calculates p_n: n-gram precision
    """
    print('Calculating p for n=', n)
    candidate_ngrams = get_ngrams_occurrences(n, candidate)
    max_ref_ngrams = {}
    for ngram in candidate_ngrams:
        for ref in references:
            ref_ngrams = get_ngrams_occurrences(n, ref)
            max_ref_ngrams[ngram] = max(max_ref_ngrams.get(ngram, 0), ref_ngrams.get(ngram, 0))
    
    # nominator
    num_ngram_matches = 0
    for ngram in candidate_ngrams:
        num_ngram_matches += min(candidate_ngrams[ngram], max_ref_ngrams[ngram])

    # denominator
    total_ngrams = sum(candidate_ngrams.values())
    res = num_ngram_matches / total_ngrams if total_ngrams > 0 else 0
    print(res)
    # for numerical reasons:
    return res if res > 0 else 1E-16


def calc_bp(ref_lens, cand_len):
    """
    Calculates brevity penalty
    """
    r = min(ref_lens, key=lambda ref_len: (abs(ref_len - cand_len), ref_len))
    print('c in bp: ', cand_len)
    print('r in bp: ', r)
    if cand_len > r:
        return 1
    else:
        return math.exp(1 - r / cand_len)


def calc_bleu(refs, cand, max_n=4, weights=[0.5, 0.5, 0, 0]):
    """
    Calculates BLEU score
    """
    precisions = []
    for i in range(1, max_n + 1):
        p = calc_p(i, refs, cand)
        precisions.append(p)
    bp = calc_bp([len(ref.split(' ')) for ref in refs], len(cand.split(' ')))
    print('bp: ', bp)
    bleu = bp * math.exp(sum(weights[i] * math.log(precisions[i]) for i in range(max_n)))
    return bleu


c = nmt_translations[0]
print('BLEU: ', calc_bleu(reference_translations, c))
print()
print('SECOND:')
c = nmt_translations[1]
print('BLEU: ', calc_bleu(reference_translations, c))