import re
from pathlib import Path
from collections import defaultdict


regex = re.compile('[^\w-]')


def wordcount(path:str):
    words = defaultdict(int)
    p = Path(path)
    if p.exists():
        with open(str(p), encoding='utf8') as f:
            for line in f:
                for word in regex.split(line):
                    if not word:
                        continue
                    words[word.lower()] += 1
    return words


if __name__ == '__main__':
    d = wordcount('D:\sample.txt')
    i = 0
    for x in sorted(d.items(), key=lambda x: x[1], reverse=True):
        if i < 10:
            print(x)
        i += 1
