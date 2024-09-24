#! /usr/bin/env python
import argparse
import random

def clean(text):
    data = text.split('\n\n')

    x = []
    for k in data:
        k = k.lower()
        k = k.replace(' ', '_')
        k = k.replace('\n', '_')
        k = k.replace('-', '_')
        k = k.replace(',', '')
        k = k.replace('\'', '')
        k = k.replace('.', '')
        x.append(k)

    return x

def fragment(text, read_length, coverage, mutation_rate):
    data = clean(text)

    chooseme = []
    for n, i in enumerate(data):
        chooseme += [n] * len(i)

    n_samples = int(len(chooseme) * coverage / float(read_length) + 0.5)

    samples = []
    for i in range(n_samples):
        seq = data[random.choice(chooseme)]

        start = random.choice(range(len(seq) - read_length))
        read = seq[start:start + read_length]

        for k in range(0, read_length):
            if random.uniform(0, 1000) < mutation_rate*1000:
                pos = random.choice(range(len(read)))
                s = ""
                for p in range(len(read)):
                    if p == pos:
                        s += random.choice('abcdefghijklmnopqrstuvwxyz_')
                    else:
                        s += read[p]
                read = s

        samples.append(read)

    return samples

def fragment_pe(text, read_length, insert_size, coverage, mutation_rate):
    data = clean(text)

    chooseme = []
    for n, i in enumerate(data):
        chooseme += [n] * len(i)

    n_samples = int(len(chooseme) * coverage / float(read_length) + 0.5)

    samples = []
    for i in range(n_samples):
        seq = data[random.choice(chooseme)]

        start = random.choice(range(len(seq) - insert_size))
        Lactual = insert_size - read_length + random.choice(range(2*read_length + 1))
        read = seq[start:start + Lactual]

        for k in range(0, insert_size):
            if random.uniform(0, 1000) < mutation_rate*1000:
                pos = random.choice(range(len(read)))
                s = ""
                for p in range(len(read)):
                    if p == pos:
                        s += random.choice('abcdefghijklmnopqrstuvwxyz_')
                    else:
                        s += read[p]
                read = s

        left, right = read[:read_length], read[-read_length:]
        samples.append((left, right))

    return samples

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('textfile')
    parser.add_argument('--randomize', action="store_true", default=False)
    args = parser.parse_args()

    text = open(args.textfile).read()
    text = clean(text)
    text = "".join(text)
    text = text.replace('_', '')

    samples = fragment(text, 30, 50, .015)

    if args.randomize:
        samples2 = []
        for s in samples:
            s = [ ch for ch in s ]
            random.shuffle(s)
            samples2.append("".join(s))
        samples = samples2

    print("\n".join(samples))

if __name__ == '__main__':
    main()
