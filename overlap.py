
def overlap(s1, s2):
    """
    :param s1: first string
    :param s2: second string
    :return: string which two input strings are substrings of or the longest string if there is no overlap

    >>> overlap('ABCDEFG', 'EFGHIJK')
    ABCDEFGHIJK
    >>> overlap('ABCDEFG', 'QWERTABC')
    QWERTABCDEFG
    >>> overlap('EFGHIJK', 'QWERTABC')
    None
    """
    maxoverlap = 0
    forward = False
    # Swap strings: s1 should be the shortest one
    if s1 > s2:
        s1, s2 = s2, s1

    # TODO: reverse directions
    # Forward
    for i in range(1, len(s1)):
        # print(s1[:i], s2[-i:])
        if s1[:i] == s2[-i:] and i > maxoverlap:
            maxoverlap = i
            forward = True
    # Backward
    for i in range(1, len(s1)):
        # print(s2[:i], s1[-i:])
        if s2[:i] == s1[-i:] and i > maxoverlap:
            maxoverlap = i
            forward = False

    # If there is no overlap
    if maxoverlap == 0:
        return None, maxoverlap

    if forward:
        return s2 + s1[maxoverlap:], maxoverlap
    else:
        return s1[:maxoverlap+1] + s2, maxoverlap


def maximal_overlap(s, string_list):
    best_overlap, maxlength = None, 0
    index = 0
    for i, string in enumerate(string_list):
        common, length = overlap(s, string.strip())
        if length > maxlength:
            best_overlap = common
            maxlength = length
            index = i
    return best_overlap, index


def assemble(string_list):
    current_string = string_list[0].strip()
    del string_list[0]
    for i in range(len(string_list)):
        current_string, index = maximal_overlap(current_string, string_list)
        del string_list[index]
        print(index, len(current_string))

    return current_string


if __name__ == '__main__':

    s1 = 'ABCDEFG'
    s2 = 'EFGHIJK'
    s3 = 'QWERTABC'

    print(overlap(s1, s2))
    print(overlap(s1, s3))
    print(overlap(s2, s3))
    print(overlap(s1, 'EFG'))

    print(assemble([s1, s2, s3]))

    g1 = 'BIBTSTNOBNTNBSNBNTNSISITNIBBITBNIITOOSNNTNBOINOSNNOOBTBOTTITNSONNSBSBNINNNSNBBBTNSISSTONIITBSISONBBTOBINBISOTTONBNBNIOBOTITIONBNTSBNNIOTBBSTBNNISTNNSIOI'
    g392 = 'NOOBNTNONOBBIBBBNTNBNIBNNBIBNOBSNBTSNTSTTIBBBIOBSISIOTNBONTBNSSSTTTSTNONTSTTTBSBNIBBIBOTSNINNOISBBSOTNNTTNBBNTNTNONBONIIITIOTISITNSTTNBNIOONIOOTISNNNNSOB'

    print(overlap(g1, g392))