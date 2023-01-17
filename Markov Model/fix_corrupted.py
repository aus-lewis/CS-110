from markov_model import MarkovModel
import stdio
import sys


# Entry point.
def main():
    # accept k (int) and s (str) as command-line arguments
    k = int(sys.argv[1])
    s = str(sys.argv[2])

    # set text to read from standard input
    text = sys.stdin.read()
    # create markov model using text and k
    model = MarkovModel(text, k)

    # decode corrupted and write to standard output
    r = model.replace_unknown(s)
    stdio.writeln(r)


if __name__ == '__main__':
    main()
