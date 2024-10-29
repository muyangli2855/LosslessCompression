import time
import os
import ctypes

# Load the zlib shared library
zlib = ctypes.CDLL("zlib1.dll" if os.name == 'nt' else "libz.so.1")

# Constants for compression level
Z_BEST_COMPRESSION = 9
CHUNK_SIZE = 1024 * 1024  # 1 MB for chunk processing

# Compression function using ctypes to call zlib
def compress(input_file, compressed_file):
    with open(input_file, 'rb') as fin:
        data = fin.read()

    # Allocate memory for the compressed data
    data_size = len(data)
    compressed_size = data_size + (data_size // 10) + 12  # Estimate for output size

    compressed_data = ctypes.create_string_buffer(compressed_size)

    # Compress the data
    zlib.compress2(ctypes.byref(compressed_data),
                   ctypes.c_ulong(compressed_size),
                   data,
                   len(data),
                   Z_BEST_COMPRESSION)

    with open(compressed_file, 'wb') as fout:
        fout.write(compressed_data.raw)

# Decompression function using ctypes to call zlib
def decompress(compressed_file, output_file):
    with open(compressed_file, 'rb') as fin:
        compressed_data = fin.read()

    # Estimate the decompressed size (you may need a larger estimate)
    decompressed_size = len(compressed_data) * 5  # Guessing max decompressed size

    decompressed_data = ctypes.create_string_buffer(decompressed_size)

    # Decompress the data
    zlib.uncompress(ctypes.byref(decompressed_data),
                    ctypes.c_ulong(decompressed_size),
                    compressed_data,
                    len(compressed_data))

    with open(output_file, 'wb') as fout:
        fout.write(decompressed_data.raw)

# Calculate file sizes and compression ratio
def compression_ratio(input_file, compressed_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    return compressed_size / input_size

# Verify if two files are identical
def files_are_equal(file1, file2):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        return f1.read() == f2.read()

# Main function
if __name__ == "__main__":
    input_file = '../test.txt'  # Change to your input file path
    compressed_file = 'compressed.custom'
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
