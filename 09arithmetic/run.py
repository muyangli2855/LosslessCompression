import struct
import time
import os
from decimal import Decimal, getcontext

# 设置浮点数精度
getcontext().prec = 100

# 压缩函数
def arithmetic_compress(input_file, compressed_file):
    with open(input_file, 'r') as fin:
        data = fin.read()

    # 生成频率表
    frequency = {}
    for char in data:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    # 计算每个字符的概率
    total_count = sum(frequency.values())
    probabilities = {char: Decimal(frequency[char]) / Decimal(total_count) for char in frequency}

    # 计算累积分布函数 (CDF)
    cdf = {}
    low = Decimal(0)
    for char, prob in probabilities.items():
        cdf[char] = (low, low + prob)
        low += prob

    # 算术编码
    low, high = Decimal(0), Decimal(1)
    for char in data:
        char_low, char_high = cdf[char]
        range_width = high - low
        high = low + range_width * char_high
        low = low + range_width * char_low

        # 对区间进行缩放，以避免精度损失
        while high < Decimal(0.5) or low > Decimal(0.5):
            if high < Decimal(0.5):
                low *= 2
                high *= 2
            elif low > Decimal(0.5):
                low = (low - Decimal(0.5)) * 2
                high = (high - Decimal(0.5)) * 2

        # 检查区间宽度，并防止溢出
        if (high - low) < Decimal('1e-50'):
            break

    # 将最终编码的值存储为字符串表示形式
    code_value = (low + high) / 2
    code_value_str = str(code_value)

    # 写入频率表和编码值
    with open(compressed_file, 'wb') as fout:
        fout.write(struct.pack('>I', len(frequency)))  # 写入频率表长度
        for char, freq in frequency.items():
            fout.write(struct.pack('>cI', char.encode(), freq))  # 写入字符和频率
        # 写入编码值
        code_value_bytes = code_value_str.encode('utf-8')
        fout.write(struct.pack('>I', len(code_value_bytes)))
        fout.write(code_value_bytes)

# 解压缩函数
def arithmetic_decompress(compressed_file, output_file):
    with open(compressed_file, 'rb') as fin:
        # 读取频率表
        frequency_length = struct.unpack('>I', fin.read(4))[0]
        frequency = {}
        for _ in range(frequency_length):
            char = struct.unpack('>c', fin.read(1))[0].decode()
            freq = struct.unpack('>I', fin.read(4))[0]
            frequency[char] = freq

        # 计算每个字符的概率
        total_count = sum(frequency.values())
        probabilities = {char: Decimal(frequency[char]) / Decimal(total_count) for char in frequency}

        # 计算累积分布函数 (CDF)
        cdf = {}
        low = Decimal(0)
        for char, prob in probabilities.items():
            cdf[char] = (low, low + prob)
            low += prob

        # 读取编码值
        code_value_length = struct.unpack('>I', fin.read(4))[0]
        code_value_str = fin.read(code_value_length).decode('utf-8')
        code_value = Decimal(code_value_str)

        # 解码
        decoded_data = []

        for _ in range(total_count):
            for char, (char_low, char_high) in cdf.items():
                if char_low <= code_value < char_high:
                    decoded_data.append(char)
                    range_width = char_high - char_low
                    code_value = (code_value - char_low) / range_width

                    # 对区间进行缩放，以避免精度损失
                    while code_value < Decimal(0) or code_value >= Decimal(1):
                        if code_value < Decimal(0.5):
                            code_value *= 2
                        elif code_value >= Decimal(0.5):
                            code_value = (code_value - Decimal(0.5)) * 2
                    break

        # 写入解码后的数据
        with open(output_file, 'w') as fout:
            fout.write(''.join(decoded_data))

# 计算文件大小和压缩比
def compression_ratio(input_file, compressed_file):
    input_size = os.path.getsize(input_file)
    compressed_size = os.path.getsize(compressed_file)
    return compressed_size / input_size

# 验证两个文件是否相同
def files_are_equal(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        return f1.read() == f2.read()

# 主函数
if __name__ == "__main__":
    input_file = '../test.txt'
    compressed_file = 'compressed.arith'
    output_file = 'out.txt'

    # 压缩
    start_time = time.time()
    try:
        arithmetic_compress(input_file, compressed_file)
    except OverflowError:
        print("Overflow occurred during compression. Adjusting precision or input size may help.")
        exit(1)
    compress_time = time.time() - start_time
    print(f"Compression time: {compress_time:.4f} seconds")

    # 解压缩
    start_time = time.time()
    arithmetic_decompress(compressed_file, output_file)
    decompress_time = time.time() - start_time
    print(f"Decompression time: {decompress_time:.4f} seconds")

    # 压缩比
    ratio = compression_ratio(input_file, compressed_file)
    print(f"Compression ratio: {ratio:.4f}")

    # 验证正确性
    if files_are_equal(input_file, output_file):
        print("Success: The decompressed file matches the original input file.")
    else:
        print("Error: The decompressed file does not match the original input file.")
