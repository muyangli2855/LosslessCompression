#!/usr/bin/python

import struct
import time
import os

# Initialize our list of phrases
phrases = (
    'the', 'and', 'to', 'was', 'you', 'that', 'of', 'with', 'have', 'her',
    'had', 'not', 'in', 'she', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
    'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
    'x', 'y', 'z', '\n', ' ', '!', '"', '&', "'", '(', ')', ',', '-', '.',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '?'
)

prefices = list(enumerate(phrases))


# Function to find the longest phrase that is a prefix of the string
def find_encoding(en, string):
    for k, w in en:
        if string.startswith(w):
            return w, k


# Compression function
def compress(input_file, compressed_file):
    with open(input_file, 'r') as fin, open(compressed_file, 'wb') as fout:
        data = fin.read()
        sextuple = 0
        encoding = 0
        outbytes = bytearray(4)

        while len(data) > 0:
            if sextuple < 4:
                s, t = find_encoding(prefices, data)
                data = data[len(s):]
                encoding += t << (6 * sextuple)
                sextuple += 1
            else:
                outbytes = struct.pack("<I", encoding)
                fout.write(outbytes[0:3])
                sextuple = 0
                encoding = 0

        # Handle any remaining bits (if data wasn't divisible by 4)
        if sextuple > 0:
            outbytes = struct.pack("<I", encoding)
            fout.write(outbytes[0:(sextuple * 6 + 7) // 8])  # Write the correct number of bytes


# Decompression function
def decompress(compressed_file, output_file):
    with open(compressed_file, 'rb') as fin, open(output_file, 'w') as fout:
        indata = fin.read()

        while len(indata) > 0:
            to_read = min(3, len(indata))  # Read up to 3 bytes, depending on available data
            buffer = indata[:to_read] + b'\0' * (3 - to_read)  # Pad with zeros if needed

            # Unpack only if there is sufficient data (always at least 1 byte)
            if len(buffer) > 0:
                fourphrases = struct.unpack("<I", buffer + b'\0')[0]  # Pad to 4 bytes for unpacking

            indata = indata[to_read:]  # Move the pointer

            # Process each 6-bit chunk in fourphrases
            for i in range(0, 4):
                ind = (fourphrases >> 6 * i) & 63
                if len(indata) == 0 and ind == 0:
                    break  # Stop if padding from the last chunk
                fout.write(phrases[ind])


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
    input_file = '../test.txt'
    compressed_file = 'compressed'
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
