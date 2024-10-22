import time
import os
import zstandard as zstd


# Zstandard Compression function
def compress(input_file, compressed_file):
    with open(input_file, 'rb') as fin:
        data = fin.read()

        # Create a Zstandard compressor object
        compressor = zstd.ZstdCompressor()

        # Compress the data
        compressed_data = compressor.compress(data)

    with open(compressed_file, 'wb') as fout:
        fout.write(compressed_data)


# Zstandard Decompression function
def decompress(compressed_file, output_file):
    with open(compressed_file, 'rb') as fin:
        compressed_data = fin.read()

        # Create a Zstandard decompressor object
        decompressor = zstd.ZstdDecompressor()

        # Decompress the data
        decompressed_data = decompressor.decompress(compressed_data)

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
    compressed_file = 'compressed.zst'
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
