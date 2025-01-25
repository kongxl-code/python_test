A = [{'module': 'F', 'dependency': 'X', 'status': True}, {'module': 'R', 'dependency': 'D', 'status': True}, {'module': 'R', 'dependency': 'Q', 'status': True}, {'module': 'Y', 'dependency': 'D', 'status': True}, {'module': 'M', 'dependency': 'L', 'status': True}, {'module': 'V', 'dependency': 'T', 'status': True}]
B = [{'module': 'F', 'dependency': 'X', 'status': True}, {'module': 'R', 'dependency': 'D', 'status': True}, {'module': 'R', 'dependency': 'Q', 'status': True}, {'module': 'Y', 'dependency': 'D', 'status': True}, {'module': 'M', 'dependency': 'L', 'status': True}]

new_list = [item for item in A if item not in B]

print(new_list)