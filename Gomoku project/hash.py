def left_rotate(s, d):
    tmp = s[d:] + s[0: d]
    return tmp


def bin_add(a, b):
    binary_sum = lambda a, b: bin(int(a, 2) + int(b, 2))

    return binary_sum(a, b)[2:]


def divide_chunks(a, n):
    for i in range(0, len(a), n):
        yield a[i:i + n]


def makeEqualLength(a, b):
    len_a = len(a)
    len_b = len(b)

    num_zeros = abs(len_a - len_b)

    if (len_a < len_b):
        for i in range(num_zeros):
            a = '0' + a
        return len_b, a, b
    else:
        for i in range(num_zeros):
            b = '0' + b
    return len_a, a, b


def orOperation(n1, n2):
    length, n1, n2 = makeEqualLength(n1, n2)
    result = ""
    for i in range(length):
        result = result + str(int(n1[i]) | int(n2[i]))

    return result


def xorOperation(n1, n2):
    length, n1, n2 = makeEqualLength(n1, n2)
    result = ""
    for i in range(length):
        result = result + str(int(n1[i]) ^ int(n2[i]))

    return result


def andOperation(n1, n2):
    length, n1, n2 = makeEqualLength(n1, n2)
    result = ""
    for i in range(length):
        result = result + str(int(n1[i]) & int(n2[i]))

    return result


def notOperation(n1):
    result = ""
    for i in range(len(n1)):
        result = result + str(int(n1[~i]))

    return result


def hashf(pw):
    h0 = "01100111010001010010001100000001"
    h1 = "11101111110011011010101110001001"
    h2 = "10011000101110101101110011111110"
    h3 = "00010000001100100101010001110110"
    h4 = "11000011110100101110000111110000"
    a = h0
    b = h1
    c = h2
    d = h3
    e = h4
    list_of_password = []
    for l in pw:
        list_of_password.append(format(ord(l), "b"))
    padded_list = (str(i).rjust(8, '0') for i in list_of_password)
    bin_password = ''.join(padded_list) + '1'
    len_of_password = len(pw)
    bin_pl = format(len_of_password, "b")
    if len_of_password < 448:
        padded_password = bin_password.ljust(448, '0')
        padded_lop = bin_pl.zfill((64))
        padded_fst_string = padded_password + ''.join(padded_lop)
        splited_chunk = list(divide_chunks(padded_fst_string, 32))
        for i in range(16, 80):
            wordA = splited_chunk[i - 3]
            wordB = splited_chunk[i - 8]
            wordC = splited_chunk[i - 14]
            wordD = splited_chunk[i - 16]

            xorA = xorOperation(wordA, wordB)
            xorB = xorOperation(xorA, wordC)
            xorC = xorOperation(xorB, wordD)
            new_word = left_rotate(xorC, 1)
            splited_chunk.append(new_word)
        for i in range(80):
            if i < 20:
                BandC = andOperation(b, c)
                notBandD = andOperation(notOperation(b), d)
                f = orOperation(BandC, notBandD)
                k = '01011010100000100111100110011001'
            elif i < 40:
                BxorC = xorOperation(b, c)
                f = xorOperation(BxorC, d)
                k = '01101110110110011110101110100001'
            elif i < 60:
                BandC = andOperation(b, c)
                BandD = andOperation(b, d)
                CandD = andOperation(c, d)
                BandC_or_BandD = orOperation(BandC, BandD)
                f = orOperation(BandC_or_BandD, CandD)
                k = '10001111000110111011110011011100'
            elif i < 80:
                BxorC = xorOperation(b, c)
                f = xorOperation(BxorC, d)
                k = '11001010011000101100000111010110'

            word = splited_chunk[i]
            tempA = bin_add(left_rotate(a, 5), f)
            tempB = bin_add(tempA, e)
            tempC = bin_add(tempB, k)
            temp = bin_add(tempC, word)

            temp = temp[slice(0, 32)]
            e = d
            d = c
            c = left_rotate(b, 30)
            b = a
            a = temp
        h0 = bin_add(h0, a)[slice(0, 32)]
        h1 = bin_add(h1, b)[slice(0, 32)]
        h2 = bin_add(h2, c)[slice(0, 32)]
        h3 = bin_add(h3, d)[slice(0, 32)]
        h4 = bin_add(h4, e)[slice(0, 32)]
    h0_hex = hex(int(h0, 2))[2:]
    h1_hex = hex(int(h1, 2))[2:]
    h2_hex = hex(int(h2, 2))[2:]
    h3_hex = hex(int(h3, 2))[2:]
    h4_hex = hex(int(h4, 2))[2:]

    return ''.join([h0_hex, h1_hex, h2_hex, h3_hex, h4_hex])
