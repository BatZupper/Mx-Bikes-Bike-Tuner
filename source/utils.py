def parse_cfg(text):
    root = {}
    stack = [root]
    current = root

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("//") or line.startswith(";"):
            continue

        if line.endswith("{"):
            key = line[:-1].strip()
            new_block = {}
            # Se la chiave esiste già come dict, usiamola; altrimenti creiamo
            if key in current and isinstance(current[key], dict):
                new_block = current[key]
            else:
                current[key] = new_block
            stack.append(new_block)
            current = new_block

        elif line == "}":
            if len(stack) > 1:
                stack.pop()
                current = stack[-1]
            else:
                current = root  # fallback di sicurezza

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