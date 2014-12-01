import random

def main():
    a = list()
    for i in range(10):
        a.append(random.choice([str("Hello!"), float("-inf")]))
    print a

main()
