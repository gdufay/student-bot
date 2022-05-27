def levenshtein(a, b):
    """
    Naive implementation of Levenshtein algorithm.
    Calculate distance between two words.
    """
    # if a empty, we return len of b
    if not len(a):
        return len(b)

    # if b empty, we return len of a
    if not len(b):
        return len(a)

    if a[0] == b[0]:
        return levenshtein(a[1:], b[1:])

    return 1 + min(levenshtein(a[1:], b), levenshtein(a, b[1:]), levenshtein(a[1:], b[1:]))

def calc_distance(s, words):
    """Return the nearest word in a given list"""
    # calculate the distance for each word
    dists = enumerate(map(lambda w: levenshtein(s, w), words))
    # retrieve the index of the littlest distance
    idx, _ = min(dists, key=lambda d: d[1])

    return words[idx]

# def lev(a, b):
#     v0 = [i for i in range(len(b) + 1)]
#     v1 = v0.copy()
# 
#     for i in range(len(a)):
#         v1[0] =  i + 1
# 
#         for j in range(len(b)):
#             del_cost = v0[j + 1] + 1
#             insert_cost = v1[j] + 1
# 
#             if a[i] == b[j]:
#                 subst_cost = v0[j]
#             else:
#                 subst_cost = v0[j] + 1
# 
#             v1[j + 1] = min(del_cost, insert_cost, subst_cost)
# 
#         tmp = v0
#         v0 = v1
#         v1 = tmp
# 
#     return v0[len(b)]
