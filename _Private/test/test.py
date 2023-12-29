import pyperclip

with open("text.txt", "r") as f:
    text = f.read()
    output = ""

    x = text.split("def ")[1:]
    for a in x:
        b = a.split("(self)")[0].upper()

        v1 = b.split("_")[-2]
        v2 = b.split("_")[-1]

        range = f"({v1}, {v2})" if v1.isnumeric() else f"({v2})"

        path = a.split('r"')[1].split('",')[0]

        try:
            modifier = f' time_modifiers=TimeModifiers(time_modifier=-0.2, end_time_modifier={a.split("self.end_time_modifier = ")[1]}),'
        except Exception:
            modifier = ""

        joe = f'{b} = Preset(r"{path}", {range},{modifier})'
        print(joe)
        # output += f'{b} = Preset(r"{path}"), {range},{modifier}'
    # pyperclip.copy(output)
