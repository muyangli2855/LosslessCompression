import time
import os

# Initialize the maximum dictionary size for LZW (commonly set as 4096 for 12-bit codes)
MAX_DICT_SIZE = 4096

# Compression function using Lempel-Ziv-Welch (LZW) algorithm
def compress(input_file, compressed_file):
    # Initialize dictionary with single character strings
    dictionary = {chr(i): i for i in range(256)}
    dict_size = 256
    string = ""
    compressed_data = []

    with open(input_file, 'r') as fin:
        data = fin.read()
        for symbol in data:
            string_plus_symbol = string + symbol
            if string_plus_symbol in dictionary:
                string = string_plus_symbol
            else:
                compressed_data.append(dictionary[string])
                if dict_size < MAX_DICT_SIZE:
                    dictionary[string_plus_symbol] = dict_size
                    dict_size += 1
                string = symbol

        # Output the code for the last string
        if string:
            compressed_data.append(dictionary[string])

    # Write the compressed data to file
    with open(compressed_file, 'wb') as fout:
        for data in compressed_data:
            fout.write(data.to_bytes(2, byteorder='big'))

# Decompression function using LZW algorithm
def decompress(compressed_file, output_file):
    # Initialize the dictionary with single character strings
    dictionary = {i: chr(i) for i in range(256)}
    dict_size = 256
    decompressed_data = []

    with open(compressed_file, 'rb') as fin:
        compressed_data = []
        byte = fin.read(2)
        while byte:
            compressed_data.append(int.from_bytes(byte, byteorder='big'))
            byte = fin.read(2)

    # Read the first value and initialize
    string = chr(compressed_data.pop(0))
    decompressed_data.append(string)

    for code in compressed_data:
        if code in dictionary:
            entry = dictionary[code]
        elif code == dict_size:
            entry = string + string[0]
        else:
            raise ValueError("Invalid compressed code")

        decompressed_data.append(entry)

        # Add new string to the dictionary
        if dict_size < MAX_DICT_SIZE:
            dictionary[dict_size] = string + entry[0]
            dict_size += 1

        string = entry

    # Write the decompressed data to file
    with open(output_file, 'w') as fout:
        fout.write(''.join(decompressed_data))


# Calculate file sizes and compression ratio
def compression_ratio(input_file, compressed_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    return compressed_size / input_size


# Verify if two files are identical
def files_are_equal(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        return f1.read() == f2.read()


# Main function
if __name__ == "__main__":
    input_file = '../test.txt'  # Change to your input file path
    compressed_file = 'compressed.lzw'
    output_file = 'out.txt'

    # Compression
    start_time = time.time()
    compress(input_file, compressed_file)
    compress_time = time.time() - start_time
    print(f"Compression time: {compress_time:.4f} seconds")

    # Decompression
    start_time = time.time()
    decompress(compressed_file, output_file)
    decompress_time = time.time() - start_time
    print(f"Decompression time: {decompress_time:.4f} seconds")

    # Compression ratio
    ratio = compression_ratio(input_file, compressed_file)
    print(f"Compression ratio: {ratio:.4f}")

    # Verify correctness
    if files_are_equal(input_file, output_file):
        print("Success: The decompressed file matches the original input file.")
    else:
        print("Error: The decompressed file does not match the original input file.")
