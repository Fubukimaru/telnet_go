from go import Go

go = Go()

while True:
    while go.status == 0:
        print(go.go_black_round_init())
        move = input()
        msg = go.go_black_round(move)
        print(msg)
    print("Press enter to continue")
    input()
    print(go.go_white_round())
