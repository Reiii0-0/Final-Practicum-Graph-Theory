import sys

class Node:
    def __init__(self, value, index):
        self.value = value
        self.index = index
        self.children = []

def build_lmis_tree(data):
    root = Node(-1, -1) 
  
    def populate_children(current_node):
        start_index = current_node.index
        
        for i in range(start_index + 1, len(data)):
          
            if data[i] > current_node.value:
                child = Node(data[i], i)
                current_node.children.append(child)
                populate_children(child)

    populate_children(root)
    return root

def find_longest_path(node):
    if not node.children:
        return [node.value] if node.value != -1 else []

    longest_subsequence = []

    for child in node.children:
        child_path = find_longest_path(child)
        if len(child_path) > len(longest_subsequence):
            longest_subsequence = child_path
            
    if node.value != -1:
        return [node.value] + longest_subsequence
    else:
        return longest_subsequence

if __name__ == "__main__":
    print("LMIS")
    print("Masukkan deret angka dipisahkan dengan SPASI.")
    print("Contoh: 4 1 13 7 0 2 8 11 3")
    
    try:
        raw_input = input(">> Masukkan angka: ")
        
        sequence = list(map(int, raw_input.split()))
        
        if not sequence:
            print("Error: Input tidak boleh kosong.")
        else:
            print(f"\nMemproses urutan: {sequence}")

            tree_root = build_lmis_tree(sequence)

            result = find_longest_path(tree_root)
          
            print(f"-" * 30)
            print(f"Hasil Subsequence Terpanjang : {result}")
            print(f"Panjang Subsequence          : {len(result)}")
            print(f"-" * 30)

    except ValueError:
        print("\n[!] Error: Pastikan Anda hanya memasukkan angka bulat yang dipisahkan spasi.")
