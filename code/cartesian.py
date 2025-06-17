def cartesian_product(x: int) -> list[list[int]]:
    """Return [v for v in itertools.product([0,1,2], repeat=x)]"""
    result = [
        [0],
        [1],
        [2]
    ]
    
    for _ in range(x - 1):
        tmp = []
        for tt in result:
            tmp.append(tt + [0])
            tmp.append(tt + [1])
            tmp.append(tt + [2])
        result = tmp
    
    return result 