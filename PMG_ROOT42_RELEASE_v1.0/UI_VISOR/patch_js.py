with open("visor.js", "r") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if "state.initNodes();" in line:
        new_lines.append("state.loadRecord();\n")
    else:
        new_lines.append(line)

with open("visor.js", "w") as f:
    f.writelines(new_lines)
