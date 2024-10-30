import gzip
import bz2
import lzma
import zstandard as zstd
import brotli
import os

# File paths
source_file = "../test.txt"
compressed_files = {
    'gzip': 'compressed_gzip',
    'bz2': 'compressed_bz2',
    'lzma': 'compressed_lzma',
    'zstd': 'compressed_zstd',
    'brotli': 'compressed_brotli'
}
decompressed_file = "output.txt"

# Function to get file size
def get_file_size(file_path):
    return os.path.getsize(file_path)

# Compress using gzip
with open(source_file, 'rb') as f_in, gzip.open(compressed_files['gzip'], 'wb') as f_out:
    f_out.write(f_in.read())

# Compress using bz2
with open(source_file, 'rb') as f_in, bz2.open(compressed_files['bz2'], 'wb') as f_out:
    f_out.write(f_in.read())

# Compress using lzma
with open(source_file, 'rb') as f_in, lzma.open(compressed_files['lzma'], 'wb') as f_out:
    f_out.write(f_in.read())

# Compress using Zstandard
with open(source_file, 'rb') as f_in, open(compressed_files['zstd'], 'wb') as f_out:
    compressor = zstd.ZstdCompressor(level=22)  # Level 22 for maximum compression
    f_out.write(compressor.compress(f_in.read()))

# Compress using Brotli
with open(source_file, 'rb') as f_in, open(compressed_files['brotli'], 'wb') as f_out:
    f_out.write(brotli.compress(f_in.read(), quality=11))  # Quality 11 for maximum compression

# Calculate and display compression rates
original_size = get_file_size(source_file)
compression_rates = {algo: get_file_size(compressed_files[algo]) / original_size for algo in compressed_files}
print("Compression rates:", compression_rates)

# Select the best compression method based on the smallest file size
best_algo = min(compression_rates, key=compression_rates.get)
print(f"Best compression algorithm: {best_algo}")

# Decompress the best compressed file and compare with the original
if best_algo == 'gzip':
    with gzip.open(compressed_files['gzip'], 'rb') as f_in, open(decompressed_file, 'wb') as f_out:
        f_out.write(f_in.read())
elif best_algo == 'bz2':
    with bz2.open(compressed_files['bz2'], 'rb') as f_in, open(decompressed_file, 'wb') as f_out:
        f_out.write(f_in.read())
elif best_algo == 'lzma':
    with lzma.open(compressed_files['lzma'], 'rb') as f_in, open(decompressed_file, 'wb') as f_out:
        f_out.write(f_in.read())
elif best_algo == 'zstd':
    with open(compressed_files['zstd'], 'rb') as f_in, open(decompressed_file, 'wb') as f_out:
        decompressor = zstd.ZstdDecompressor()
        f_out.write(decompressor.decompress(f_in.read()))
elif best_algo == 'brotli':
    with open(compressed_files['brotli'], 'rb') as f_in, open(decompressed_file, 'wb') as f_out:
        f_out.write(brotli.decompress(f_in.read()))

# Verify if decompressed file matches the original
with open(source_file, 'rb') as f_original, open(decompressed_file, 'rb') as f_decompressed:
    if f_original.read() == f_decompressed.read():
        print("success")
    else:
        print("failure")
