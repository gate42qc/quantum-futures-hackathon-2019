def binStrToInt(binary_str):


    """The function binStrToInt() takes in one input, a string of ones and
    zeros (no spaces) called BINARY_STR.  It treats that input as a binary
    number (base 2) and converts it to a decimal integer (base 10). It
    returns an integer result."""

    length = len(binary_str)

    num = 0
    for i in range(length):
        num = num + int(binary_str[i])
        num = num * 2
    return int(num / 2)
