import heap

def generate_frequency_table(msg):
  table = {}
  for i in range(len(msg)):
    c = msg[i]
    if c not in table:
      table[c] = 1
    else:
      table[c] += 1
  return table

def create_huffman(freq_table):
  pq = heap.Heap()
  for key, value in freq_table.items():
    pq.insert( (value, key, None, None))

  while pq.get_size() > 1:
    item1 = pq.remove_min()
    item2 = pq.remove_min()
    new_value = item1[0] + item2[0]
    new_item = (new_value, '', item1, item2)
    pq.insert(new_item)

  huffman_tree = pq.remove_min()
  # traverse tree and build two dicts
  encoding = {} # symbol to num
  decoding = {} # num to symbol
  def dfs(node, val):
    key = node[1]
    if key != '':
      encoding[key] = val
      decoding[val]= key
    if node[2]:
      dfs(node[2], val + '0')
    if node[3]:
      dfs(node[3], val + '1')
  dfs(huffman_tree, '')
  return encoding, decoding

def huffman_encode(msg, code):
  encoding = code[0]
  str = ''
  for i in range(len(msg)):
    if msg[i] not in encoding:
      raise ValueError("The message is unable to be encoded")
    str += encoding[msg[i]]
  return str

def huffman_decode(msg, code):
  decoding = code[1]
  str = ''
  i = 0
  j = 0
  while i < len(msg):
    if msg[i:j] not in decoding:
      j += 1
      if j > len(msg):
        raise ValueError("The message is unable to be decoded")
    else:
      str += decoding[msg[i:j]]
      i = j
      j = i
  return str

if __name__ == "__main__":
  message = "this is an example of a huffman tree"
  print(f'original message: {message}')
  table = generate_frequency_table(message)
  code = create_huffman(table)
  print(f'encoding dict: {code[0]}')
  print(f'decoding dict: {code[1]}')
  encoded = huffman_encode(message, code)
  print(f'encoded message: {encoded}')
  print(f'encoded length: {len(encoded)}')
  decoded = huffman_decode(encoded, code)
  print(f'decoded message: {decoded}')
