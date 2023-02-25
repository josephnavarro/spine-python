#! usr/bin/env python3


def binarySearch(values, target, step: int):
    low: int = 0
    high: int = int(len(values) / step - 2)

    if high == 0:
        return step
    else:
        current: int = high >> 1
        while True:
            if values[(current + 1) * step] <= target:
                low = current + 1
            else:
                high = current

            if low == high:
                return (low + 1) * step

            current = int((low + high) >> 1)
        # return 0
