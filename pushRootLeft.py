
class PushRootLeft:
    def __init__(self, positions=42):
        self.positions = positions

    def __call__(self, s):
        result = []
        for line in s.splitlines(True):
            sline = line.strip()
            if not sline or sline[0] == '#':
                result.append(line)
            else:
                result.append(' ' * self.positions + line)
        return ''.join(result)

