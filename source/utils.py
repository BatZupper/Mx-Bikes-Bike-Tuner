def parse_cfg(text):
    root = {}
    stack = [root]
    current = root

    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith("//") or line.startswith(";"):
            continue

        if line.endswith("{"):
            key = line[:-1].strip()
            new_block = {}
            current[key] = new_block
            stack.append(new_block)
            current = new_block

        elif line == "}":
            stack.pop()
            if stack:
                current = stack[-1]
            else:
                current = root

        elif "=" in line:
            k, v = [p.strip() for p in line.split("=", 1)]
            current[k] = v

    return root


def dump_cfg(data, indent=0):
    lines = []
    for k, v in data.items():
        if isinstance(v, dict):
            lines.append(" " * indent + f"{k} {{")
            lines.append(dump_cfg(v, indent + 4))
            lines.append(" " * indent + "}")
        else:
            lines.append(" " * indent + f"{k} = {v}")
    return "\n".join(lines)