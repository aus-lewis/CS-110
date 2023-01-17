import symboltable
from symboltable import SymbolTable
import stdio
import stdrandom
import sys


class MarkovModel(object):
    # Creates a Markov model of order k from the given text.
    def __init__(self, text, k):
        self._k = k
        self._st = {}
        circ_text = text + text[:k]
        for i in range(len(circ_text) - k):
            self._st.setdefault(circ_text[i:i + k], {})
            self._st[circ_text[i:i + k]].setdefault(circ_text[k + i], 0)
            self._st[circ_text[i:i + k]][circ_text[k + i]] += 1

    # Returns the order this Markov model.
    def order(self):
        return self._k

    # Returns the number of occurrences of kgram in this Markov model; and 0 if kgram is
    # nonexistent. Raises an error if kgram is not of length k.
    def kgram_freq(self, kgram):
        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' + str(self._k))
        if kgram not in self._st:
            return 0
        a = list(self._st[kgram].values())
        a = sum(a)
        return a

    # Returns number of times character c follows kgram in this Markov model; and 0 if kgram is
    # nonexistent or if it is not followed by c. Raises an error if kgram is not of length k.
    def char_freq(self, kgram, c):
        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' + str(self._k))
        if kgram not in self._st:
            return 0
        if c not in self._st[kgram]:
            return 0
        return self._st[kgram][c]

    # Returns a random character following kgram in this Markov model. Raises an error if kgram is
    # not of length k or if kgram is nonexistent.
    def rand(self, kgram):
        if self._k != len(kgram):
            raise ValueError('kgram ' + kgram + ' not of length ' + str(self._k))
        if kgram not in self._st:
            raise ValueError('Unknown kgram ' + kgram)
        a = list(self._st[kgram].values())
        s = sum(a)
        for i in range(len(a)):
            a[i] = a[i] / float(s)
        d = stdrandom.discrete(a)
        a = list(self._st[kgram].keys())
        return a[d]

    # Generates and returns a string of length n from this Markov model, the first k characters of
    # which is kgram.
    def gen(self, kgram, n):
        text = kgram
        while len(text) < n:
            text += self.rand(text[-self.order():])
        return text

    # Replaces unknown characters (~) in corrupted with most probable characters from this Markov
    # model, and returns that string.
    def replace_unknown(self, corrupted):
        original = ''
        for i in range(len(corrupted)):
            if corrupted[i] == '~':
                a = i - self._k
                kgram_before = corrupted[a:i]
                kgram_after = corrupted[i + 1: self._k + i + 1]
                char_after = list(self._st[kgram_before].keys())
                probs = []
                for v in char_after:
                    context = kgram_before + v + kgram_after
                    p = 1.0
                    for i in range(self._k + 1):
                        kgram = context[i:self._k + i]
                        char = context[i + self._k]
                        if (kgram not in self._st or char not in self._st[kgram]):
                            p = 0
                            break
                        else:
                            q = self.char_freq(kgram, char) / float(self.kgram_freq(kgram))
                            p *= q
                    probs += [p]
                original += char_after[_argmax(probs)]
            else:
                original += corrupted[i]
        return original


# Given a list a, _argmax returns the index of the maximum value in a.
def _argmax(a):
    return a.index(max(a))


# Unit tests the data type [DO NOT EDIT].
def _main():
    text = sys.argv[1]
    k = int(sys.argv[2])
    model = MarkovModel(text, k)
    a = []
    while not stdio.isEmpty():
        kgram = stdio.readString()
        char = stdio.readString()
        a.append((kgram.replace('-', ' '), char.replace('-', ' ')))
    for kgram, char in a:
        if char == ' ':
            stdio.writef('freq(%s) = %s\n', kgram, model.kgram_freq(kgram))
        else:
            stdio.writef('freq(%s, %s) = %s\n', kgram, char, model.char_freq(kgram, char))


if __name__ == '__main__':
    _main()
