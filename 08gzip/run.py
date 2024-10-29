import time
import os
import gzip

# Gzip Compression function
def compress(input_file, compressed_file):
    with open(input_file, 'rb') as fin:
        data = fin.read()
        with gzip.open(compressed_file, 'wb', compresslevel=9) as fout:
            fout.write(data)

# Gzip Decompression function
def decompress(compressed_file, output_file):
    with gzip.open(compressed_file, 'rb') as fin:
        decompressed_data = fin.read()

    with open(output_file, 'wb') as fout:
        fout.write(decompressed_data)

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
    compressed_file = 'compressed.gz'
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
