import heapq
from collections import defaultdict

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def calculate_frequencies(text):
    frequencies = defaultdict(int)
    for char in text:
        frequencies[char] += 1
    return frequencies

def build_huffman_tree(frequencies):
    priority_queue = [HuffmanNode(char, freq) for char, freq in frequencies.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        node1 = heapq.heappop(priority_queue)
        node2 = heapq.heappop(priority_queue)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def generate_huffman_codes(root):
    codes = {}

    def traverse(node, code):
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = code
        traverse(node.left, code + "0")  # Go left: append "0"
        traverse(node.right, code + "1")  # Go right: append "1"

    traverse(root, "")
    return codes

def encode_text(text, codes):
    encoded_text = "".join(codes[char] for char in text)
    return encoded_text

def decode_text(encoded_text, root):
    decoded_text = []
    current_node = root
    for bit in encoded_text:
        current_node = current_node.left if bit == "0" else current_node.right
        if current_node.char is not None:
            decoded_text.append(current_node.char)
            current_node = root
    return "".join(decoded_text)

def save_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)

def read_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()

def huffman_compression(input_file, encoded_file, codes_file):
    text = read_from_file(input_file)
    frequencies = calculate_frequencies(text)
    root = build_huffman_tree(frequencies)
    codes = generate_huffman_codes(root)
    encoded_text = encode_text(text, codes)

    # Save the encoded text (binary string) to encoded_file
    save_to_file(encoded_file, encoded_text)

    # Save the Huffman codes (char to code mapping) to codes_file
    with open(codes_file, "w", encoding="utf-8") as file:
        for char, code in codes.items():
            file.write(f"{char}:{code}\n")

    # Return the root of the Huffman tree for future use during decompression
    return root

def huffman_decompression(encoded_file, root, output_file):
    # Read the encoded (binary) text from encoded_file
    encoded_text = read_from_file(encoded_file)

    # Decode the encoded text back to original characters
    decoded_text = decode_text(encoded_text, root)

    # Save the decompressed text to output_file
    save_to_file(output_file, decoded_text)

# Example usage
input_file = "input.txt"  # Original text file
encoded_file = "encoded.txt"  # Compressed text file (binary)
codes_file = "codes.txt"  # Huffman codes file
output_file = "output.txt"  # Decompressed output file

# Write input text to input.txt
save_to_file(input_file, "AAABBCCA")

# Compress the text and save to encoded.txt
root = huffman_compression(input_file, encoded_file, codes_file)

# Decompress the encoded text and save to output.txt (this should match input.txt)
huffman_decompression(encoded_file, root, output_file)

# Validate the process
print(f"Original Text: {read_from_file(input_file)}")
print(f"Encoded Text: {read_from_file(encoded_file)}")
print(f"Decompressed Text: {read_from_file(output_file)}")
