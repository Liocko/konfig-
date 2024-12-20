import argparse
import re
import yaml
import sys

def parse_config(text):
    result = {}
    global lines_iter
    lines_iter = iter(text.splitlines())

    for line in lines_iter:
        line = line.strip()
        if not line:
            continue

        if line.startswith("global"):
            match = re.match(r"global ([a-zA-Z]+)\s*=\s*(.*);", line)
            if match:
                name, value = match.groups()
                result[name] = parse_value(value)
            else:
                raise SyntaxError(f"Ошибка в объявлении глобальной константы: {line}")

        elif line == "{":
            current_dict = {}
            while True:
                line = next(lines_iter).strip()
                if line == "}":
                    break
                if line:
                    name, value = line.split("=")
                    current_dict[name.strip()] = parse_value(value.strip())
            result.update(current_dict)

        else:
            raise SyntaxError(f"Неизвестная строка: {line}")

    return result


def parse_value(value): #парсит значение
    if re.match(r'^-?\d+$', value):
        return int(value)
    elif re.match(r'^@"[^"]*"$',value):
        return value[2:-1]
    elif value == "{}":
        return {}
    else:
        raise ValueError(f"Unknown value: {value}")


def main():
    parser = argparse.ArgumentParser(description='YAML parser.')
    parser.add_argument("-i", "--input", required=True, help="Input file path.")
    parser.add_argument("-o", "--output", required=True, help="Output file path.")
    args = parser.parse_args()

    try:
        with open(args.input, "r", encoding = "utf-8") as infile:
            text = infile.read()
            data = parse_config(text)

        with open(args.output, "w", encoding = "utf-8") as outfile:
            yaml.dump(data, outfile, allow_unicode = True)
            print(f"Wrote to {args.output}")

    except Exception as e:
        print(f"Error: {e}", file = sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main();
