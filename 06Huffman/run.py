import struct
import time
import os

# 定义哈夫曼树节点类
class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

# 为了排序，实现比较函数
def node_comparison(node1, node2):
    return node1.freq < node2.freq

# 构建哈夫曼树
def build_huffman_tree(frequency):
    nodes = [HuffmanNode(char, freq) for char, freq in frequency.items()]

    # 模拟优先队列
    while len(nodes) > 1:
        # 按照频率排序
        nodes.sort(key=lambda x: x.freq)

        # 取出频率最小的两个节点并合并
        left = nodes.pop(0)
        right = nodes.pop(0)
        merged = HuffmanNode(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right

        # 将新节点放回列表
        nodes.append(merged)

    # 返回哈夫曼树的根节点
    return nodes[0]

# 生成编码表
def generate_codes(node, prefix="", codebook={}):
    if node is None:
        return

    if node.char is not None:
        codebook[node.char] = prefix
    else:
        generate_codes(node.left, prefix + "0", codebook)
        generate_codes(node.right, prefix + "1", codebook)
    return codebook

# 压缩函数
def huffman_compress(input_file, compressed_file):
    with open(input_file, 'r') as fin:
        data = fin.read()

    # 生成频率表
    frequency = {}
    for char in data:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    # 构建哈夫曼树和编码表
    huffman_tree = build_huffman_tree(frequency)
    codebook = generate_codes(huffman_tree)

    # 编码数据
    encoded_data = ''.join([codebook[char] for char in data])

    # 写入频率表和编码数据
    with open(compressed_file, 'wb') as fout:
        fout.write(struct.pack('>I', len(frequency)))  # 写入频率表长度
        for char, freq in frequency.items():
            fout.write(struct.pack('>cI', char.encode(), freq))  # 写入字符和频率

        # 写入编码数据并填充字节
        padding_length = 8 - len(encoded_data) % 8
        encoded_data += '0' * padding_length
        fout.write(struct.pack('B', padding_length))  # 写入填充长度
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i+8]
            fout.write(struct.pack('B', int(byte, 2)))

# 解压缩函数
def huffman_decompress(compressed_file, output_file):
    with open(compressed_file, 'rb') as fin:
        # 读取频率表
        frequency_length = struct.unpack('>I', fin.read(4))[0]
        frequency = {}
        for _ in range(frequency_length):
            char = struct.unpack('>c', fin.read(1))[0].decode()
            freq = struct.unpack('>I', fin.read(4))[0]
            frequency[char] = freq

        # 重建哈夫曼树
        huffman_tree = build_huffman_tree(frequency)

        # 读取填充长度
        padding_length = struct.unpack('B', fin.read(1))[0]

        # 读取编码数据并转为二进制字符串
        encoded_data = ''
        while (byte := fin.read(1)):
            encoded_data += f"{bin(byte[0])[2:]:>08}"

        # 移除填充的0
        encoded_data = encoded_data[:-padding_length]

        # 解码数据
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

        # 写入解码后的数据
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

# 主函数
if __name__ == "__main__":
    input_file = '../test.txt'
    compressed_file = 'compressed.huff'
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
