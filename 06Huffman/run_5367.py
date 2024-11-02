import struct
import time
import os

# Define Huffman tree node class
class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

# Function for node comparison to enable sorting
def node_comparison(node1, node2):
    return node1.freq < node2.freq

# Build the Huffman tree
def build_huffman_tree(frequency):
    nodes = [HuffmanNode(char, freq) for char, freq in frequency.items()]

    # Simulate a priority queue
    while len(nodes) > 1:
        # Sort nodes by frequency
        nodes.sort(key=lambda x: x.freq)

        # Remove the two nodes with the lowest frequency and merge them
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right

        # Add the new merged node back to the list
        nodes.append(merged)

    # Return the root node of the Huffman tree
    return nodes[0]

# Generate the encoding table
def generate_codes(node, prefix="", codebook={}):
    if node is None:
        return

    if node.char is not None:
        codebook[node.char] = prefix
    else:
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

# Compression function
def huffman_compress(input_file, compressed_file):
    with open(input_file, 'r') as fin:
        data = fin.read()

    # Generate the frequency table
    frequency = {}
    for char in data:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    # Build Huffman tree and codebook
    huffman_tree = build_huffman_tree(frequency)
    codebook = generate_codes(huffman_tree)

    # Encode data
    encoded_data = ''.join([codebook[char] for char in data])

    # Write frequency table and encoded data
    with open(compressed_file, 'wb') as fout:
        fout.write(struct.pack('>I', len(frequency)))  # Write frequency table length
        for char, freq in frequency.items():
            fout.write(struct.pack('>cI', char.encode(), freq))  # Write character and frequency

        # Write encoded data and add padding bits
        padding_length = 8 - len(encoded_data) % 8
        encoded_data += '0' * padding_length
        fout.write(struct.pack('B', padding_length))  # Write padding length
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            fout.write(struct.pack('B', int(byte, 2)))

# Decompression function
def huffman_decompress(compressed_file, output_file):
    with open(compressed_file, 'rb') as fin:
        # Read the frequency table
        frequency_length = struct.unpack('>I', fin.read(4))[0]
        frequency = {}
        for _ in range(frequency_length):
            char = struct.unpack('>c', fin.read(1))[0].decode()
            freq = struct.unpack('>I', fin.read(4))[0]
            frequency[char] = freq

        # Rebuild the Huffman tree
        huffman_tree = build_huffman_tree(frequency)

        # Read the padding length
        padding_length = struct.unpack('B', fin.read(1))[0]

        # Read encoded data and convert it to a binary string
        encoded_data = ''
        while (byte := fin.read(1)):
            encoded_data += f"{bin(byte[0])[2:]:>08}"

        # Remove the padding bits
        encoded_data = encoded_data[:-padding_length]

        # Decode data
        decoded_data = []
        current_node = huffman_tree
        for bit in encoded_data:
            if bit == '0':
                current_node = current_node.left
            else:
                current_node = current_node.right

            if current_node.char:
                decoded_data.append(current_node.char)
                current_node = huffman_tree

        # Write the decoded data to the output file
        with open(output_file, 'w') as fout:
            fout.write(''.join(decoded_data))

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
    huffman_compress(input_file, compressed_file)
    compress_time = time.time() - start_time
    print(f"Compression time: {compress_time:.4f} seconds")

    # Decompression
    start_time = time.time()
    huffman_decompress(compressed_file, output_file)
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
