def pareto_compare(number_of_features: int, p_array: list, q_array: list,
                   fiz: list, max_is_best: bool):
    result = 0
    sign = -1 if (max_is_best is False) else 1

    if fiz[0] == 0:
        for i in range(number_of_features):
            if p_array[i] == q_array[i]:
                continue
            partial = sign if p_array[i] > q_array[i] else -sign
            if result == 0:
                result = partial
            elif result != partial:
                return 0
    else:
        for i in range(number_of_features):
            w_float = p_array[i] - q_array[i]
            if w_float < 0.0:
                w_float = -w_float
            if w_float <= fiz[i]:
                return 0
            partial = sign if p_array[i] > q_array[i] else -sign
            if result == 0:
                result = partial
            elif result != partial:
                return 0
    return result


def pareto_scale(population_size: int, number_of_features_in_every_sample: int,
                 feature_values_for_each_sample: list, fuziness_per_feature: list,
                 max_is_best: bool, ranks_for_each_sample: list):
    pareto_peel = 0
    pareto_card = 1
    pareto_metric = pareto_peel

    if pareto_metric == pareto_card:
        for i in range(population_size):
            for j in range(i + 1, population_size, 1):
                bf = pareto_compare(number_of_features_in_every_sample, feature_values_for_each_sample[i],
                                    feature_values_for_each_sample[j], fuziness_per_feature, max_is_best)
                if bf < 0:
                    ranks_for_each_sample[i] += 1
                elif bf > 0:
                    ranks_for_each_sample[j] += 1
    else:
        ndom = []
        for x in range(population_size):
            ndom.append(0)
        doms = []
        for x in range(population_size):
            doms.append(ndom[:])
        for i in range(population_size):
            for j in range(i + 1, population_size, 1):
                bf = pareto_compare(number_of_features_in_every_sample, feature_values_for_each_sample[i],
                                    feature_values_for_each_sample[j], fuziness_per_feature, max_is_best)
                if bf < 0:
                    ranks_for_each_sample[i] += 1
                    k = ndom[j]
                    doms[j][k] = i
                    ndom[j] += 1
                elif bf > 0:
                    ranks_for_each_sample[j] += 1
                    k = ndom[i]
                    doms[i][k] = j
                    ndom[i] += 1
        max_rank = -1
        for i in range(population_size):
            ranks_for_each_sample[i] = -1
        while True:
            iset = 0
            for i in range(population_size):
                if ranks_for_each_sample[i] <= -1:
                    for j in range(ndom[i]):
                        k = doms[i][j]
                        ranks_for_each_sample[k] -= 1
            max_rank += 1
            for i in range(population_size):
                if ranks_for_each_sample[i] >= 0:
                    continue
                if ranks_for_each_sample[i] == -1:
                    ranks_for_each_sample[i] = max_rank
                else:
                    ranks_for_each_sample[i] = -1
                    iset = 1
            if iset <= 0:
                break


def execute():
    keys = []
    data = []
    all_input = []

    input_file = open('infile.txt', 'r')
    for line in input_file:
        all_input.append(list(map(eval, line.split(' '))))
    input_file.close()
    n, f, g = all_input[0]
    fiz = []
    for x in range(n):
        fiz.append(0.0)
    maxisbest = True
    rank = []
    for x in range(n):
        rank.append(0)
    for i in range(1, n + 1):
        keys.append(all_input[i][0])
        data.append(all_input[i][1:])
        # if g != 0:
    pareto_scale(n, f, data, fiz, maxisbest, rank)

    output_file = open('outfile.txt', 'w')
    output_file.write('{0} {1} 1\n'.format(n, f))
    for i in range(n):
        output_file.write('{0}'.format(keys[i]))
        for j in range(f):
            output_file.write(' {0}'.format(data[i][j]))
        output_file.write(' : {0}\n'.format(rank[i]))
    output_file.close()


execute()
