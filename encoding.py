def encode(text: str): 
    """
    Encodes the given text into bytes using UTF-8 encoding.
    """
    return ''.join('{0:08b}'.format(ord(x), 'b') for x in text)

def decode(binary_str: str):
    """
    Decodes a binary string back into text using UTF-8 encoding.
    """
    binary_values = binary_str.split(' ')
    ascii_characters = [chr(int(bv, 2)) for bv in binary_values]
    return ''.join(ascii_characters)