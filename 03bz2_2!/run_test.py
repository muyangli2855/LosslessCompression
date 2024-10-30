import time
import os
import struct


def bwt(s):
    """Burrows-Wheeler Transform for byte sequences."""
    s = s.decode('latin1')  # Decode bytes to handle as string
    table = sorted(s[i:] + s[:i] for i in range(len(s)))
    transformed = ''.join(row[-1] for row in table)
    return transformed.encode('latin1'), table.index(s)


def ibwt(s, idx):
    """Inverse Burrows-Wheeler Transform for byte sequences."""
    s = s.decode('latin1')
    table = [''] * len(s)
    for _ in range(len(s)):
        table = [s[i] + table[i] for i in range(len(s))]
        table.sort()
    return table[idx].encode('latin1')


def mtf(s):
    """Move-to-Front encoding."""
    symbols = list(range(256))  # Full byte range for encoding
    result = []
    for byte in s:
        idx = symbols.index(byte)
        result.append(idx)
        symbols.insert(0, symbols.pop(idx))  # Move the symbol to the front
    return result


def imtf(encoded):
    """Inverse Move-to-Front decoding."""
    symbols = list(range(256))  # Full byte range for decoding
    result = []
    for idx in encoded:
        symbol = symbols[idx]
        result.append(symbol)
        symbols.insert(0, symbols.pop(idx))  # Move symbol to front
    return bytes(result)


def rle_encode(data):
    """Run-Length Encoding for final compression step."""
    encoded = []
    prev_byte = data[0]
    count = 1
    for byte in data[1:]:
        if byte == prev_byte:
            count += 1
        else:
            encoded.extend([count, prev_byte])
            prev_byte = byte
            count = 1
    encoded.extend([count, prev_byte])  # Append last run
    return bytes(encoded)


def rle_decode(data):
    """Run-Length Decoding for decompression step."""
    decoded = []
    for i in range(0, len(data), 2):
        count = data[i]
        byte = data[i + 1]
        decoded.extend([byte] * count)
    return bytes(decoded)


# 更新 compress 函数
def compress(input_file, compressed_file):
    """Read from input file, compress data using BWT, MTF, and RLE, and write to compressed file."""
    with open(input_file, 'rb') as fin:
        data = fin.read()

    # Apply BWT and MTF
    transformed, idx = bwt(data)
    encoded = mtf(transformed)
    # Apply RLE for final compression
    rle_encoded = rle_encode(encoded)

    # Write compressed data to file
    with open(compressed_file, 'wb') as fout:
        fout.write(struct.pack('>I', idx))  # Store BWT index
        fout.write(rle_encoded)  # Store RLE encoded data


# 更新 decompress 函数
def decompress(compressed_file, output_file):
    """Read from compressed file, decompress using RLE, inverse MTF and BWT, and write to output file."""
    with open(compressed_file, 'rb') as fin:
        idx = struct.unpack('>I', fin.read(4))[0]  # Read BWT index
        rle_encoded = fin.read()  # Read RLE encoded data

    # Apply RLE decode, inverse MTF and BWT
    encoded = list(rle_decode(rle_encoded))
    decoded = imtf(encoded)
    original_data = ibwt(decoded, idx)

    # Write decompressed data to output file
    with open(output_file, 'wb') as fout:
        fout.write(original_data)


# Calculate file sizes and compression ratio
def compression_ratio(input_file, compressed_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    return compressed_size / input_size


# Verify if two files are identical
def files_are_equal(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()


if __name__ == "__main__":
    input_file = '../test.txt'  # Change to your input file path
    compressed_file = 'compressed.bwt'
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
