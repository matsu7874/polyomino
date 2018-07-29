import time


import dancinglinks
import polyomino


def solve(problem, polyominos, variations):
    size = problem.y_size * problem.x_size
    subsets = []
    for pid, vs in enumerate(variations):
        for variation in vs:
            for y in range(problem.y_size - variation.y_size + 1):
                for x in range(problem.x_size - variation.x_size + 1):
                    if problem.can_add_polyomino(variation, y, x):
                        subsets.append([size + pid] + [problem.x_size * (vy + y) + x + vx for vy in range(
                            variation.y_size) for vx in range(variation.x_size) if variation.form[vy][vx]])
    problem_piece = [problem.x_size * vy + vx for vy in range(
        problem.y_size) for vx in range(problem.x_size) if problem.form[vy][vx]]
    if problem_piece:
        subsets.append([size + len(polyominos) + 1] + problem_piece)

    dl = dancinglinks.DancingLinks(
        size + len(polyominos) + (1 if problem_piece else 0), subsets)
    res = dl.algorithm_x()
    for r in sorted(res):
        ans = [subsets[x] for x in r]
        print(ans)
        cells = [['-' for x in range(problem.x_size)]
                 for y in range(problem.y_size)]
        for a in ans:
            pname = polyominos[a[0] - size].name
            for p in a[1:]:
                cells[p // problem.x_size][p % problem.x_size] = pname
        for row in cells:
            print(''.join(row))
    print('answer count:', len(res))


def main():
    problem, polyominos = polyomino.read_puzzle_2d()

    start = time.time()

    variations = [polyomino.generate_variations(p) for p in polyominos]
    solve(problem, polyominos, variations)

    elapsed = time.time() - start
    print('elapsed time: {}[s]'.format(elapsed))


if __name__ == '__main__':
    main()
