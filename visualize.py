def visualize_dice(dice_roll):
    dice_number = len(dice_roll)
    dice_display = []
    for i in range(dice_number):
        if dice_roll[i] == "worm":
            dice_display.append("w")
        else:
            dice_display.append(dice_roll[i])

    for i in range(dice_number):
        print("  ---  ", end="")
    print("")
    for i in range(dice_number):
        print(f" | {dice_display[i]} | ", end="")
    print("")
    for i in range(dice_number):
        print("  ---  ", end="")
    print("")


def old_visualize_dice(dice_roll):

    dice_number = len(dice_roll)
    dice_display = []
    for i in range(dice_number):
        if dice_roll[i] == "worm":
            dice_display.append("§")
        else:
            dice_display.append(dice_roll[i])
    print("")
    for i in range(dice_number):
        print(" ", "-"*7, " ", end="")
    print("")
    for i in range(dice_number):
        print(" ", "*     *", " ", end="")
    print("")
    for i in range(dice_number):
        print(" ", f"*  {dice_display[i]}  *", " ", end="")
    print("")
    for i in range(dice_number):
        print(" ", "*     *", " ", end="")
    print("")
    for i in range(dice_number):
        print(" ", "*"*7, " ", end="")
    print("")
