def vaccum(left,right,position):
    print("initial condition")
    print("right place",right)
    print("left place",left)
    print("position ",position)

    while left=="dirty" or right=="dirty":
        if position=="left" and left=="dirty":
            print("\nclean left")
            left="clean"
        if position=="right" and right=="dirty":
            print("\nclean right")
            right="clean"
        if position=="left" and right=="dirty":
            print("\nmove right ")
            position="right"
        if position=="right" and left=="dirty":
            print("\nmove left")
            position="left"
        print("\nright",right)
        print("left",left)
        print("position",position)
    print("\ngoal achieved ,both places are cleaned")
vaccum("dirty","dirty","left")
