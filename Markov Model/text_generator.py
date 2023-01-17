from markov_model import MarkovModel
import stdio
import sys


# Entry point.
def main():
    # accept k (int) and n (int) as command-line argument
    k = int(sys.argv[1])
    n = int(sys.argv[2])

    # set text to accept standard input
    text = sys.stdin.read()

    # create markov model and generate random text and write to standard output
    model = MarkovModel(text, k)
    z = model.gen(text[:k], n)
    stdio.writeln(z)


if __name__ == '__main__':
    main()
