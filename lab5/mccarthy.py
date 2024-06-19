def M(n: int) -> int:
    print(n, end=" ")  # for debugging

    if n > 100:
        return n - 10
    else:
        return M(M(n + 11))


def main():
    n = 99
    print()
    print("!~", M(n), "~!", sep="")
    print()


if __name__ == "__main__":
    main()
