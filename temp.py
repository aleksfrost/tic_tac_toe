
board = []
[board.append(["K" for _ in range(3)]) for _ in range(3)]
#res = "|".join([[butt for butt in row] for row in board])

print(board)
temp = []
for row in board:
    temp.extend(row)
print(temp)