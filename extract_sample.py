# extract_sample.py

def extract_sample(input_file, output_file, num_chars=2664245):
    with open(input_file, 'r') as fin:
        content = fin.read(num_chars)  # Read the specified number of characters
    with open(output_file, 'w') as fout:
        fout.write(content)

# 提取前 5000 个字符
extract_sample('austen.txt', 'test.txt')
