Kb = 1_000
KB = 8_000
Mb = 1_000_000
MB = 8_000_000
Gb = 1_000_000_000
GB = 8_000_000_000

MAX_POINTS = 10

UPWARD_COMPUTE = [200_000, 300_000, 400_000, 600_000, 800_000, 1_000_000, 1_500_000, 2_000_000, 3_000_000, 4_000_000]
PARALLEL_COMPUTE = [20_000, 40_000, 60_000, 80_000, 100_000, 200_000, 400_000, 600_000, 700_000, 800_000]
DOWNWARD_COMPUTE = [10, 50, 100, 300, 500, 1_000, 2_000, 5_000, 10_000, 20_000]

UPWARD_MEMORY = [8_000 * GB * GB, 15_000 * GB * GB, 20_000 * GB * GB, 25_000 * GB * GB, 40_000 * GB * GB,
                 50_000 * GB * GB, 75_000 * GB * GB, 100_000 * GB * GB, 200_000 * GB * GB, 300_000 * GB * GB]

PARALLEL_MEMORY = [50 * GB * GB, 100 * GB * GB, 200 * GB * GB, 400 * GB * GB, 800 * GB * GB,
                   1_600 * GB * GB, 3_200 * GB * GB, 6_400 * GB * GB, 12_800 * GB * GB, 20_000 * GB * GB]

DOWNWARD_MEMORY = [10 * MB * MB, 50 * MB * MB, 200 * MB * MB, 500 * MB * MB, 1000 * MB * MB,
                   10_000 * MB * MB, 100_000 * MB * MB, 1 * GB * GB, 10 * GB * GB, 20 * GB * GB]

UPWARD_CONN = [100*Gb, 200*Gb, 400*Gb, 600*Gb, 800*Gb,
               1000*Gb, 1250*Gb, 1500*Gb, 1750*Gb, 2000*Gb]

PARALLEL_CONN = [1*Gb, 10*Gb, 20*Gb, 30*Gb, 40*Gb,
                 50*Gb, 60*Gb, 100*Gb, 200*Gb, 400*Gb]

DOWNWARD_CONN = [100*Kb, 1*Mb, 10*Mb, 50*Mb, 100*Mb,
                 250*Mb, 500*Mb,1*Gb, 2.5*Gb, 10*Gb]

UPWARD_POWER = [1000, 750, 500, 400, 300, 250, 200, 150, 100, 50]
PARALLEL_POWER = [350, 300, 250, 200, 150, 100, 75, 50, 40, 30]
DOWNWARD_POWER = [50, 30, 10, 7.5, 5, 2.5, 1, 0.5, 0.1, 0.05]

UPWARD_PRICE = [8000, 7000, 6000, 5000, 4000, 3000, 2000, 1500, 1000, 500]
PARALLEL_PRICE = [800, 600, 500, 400, 350, 300, 250, 200, 150, 100]
DOWNWARD_PRICE = [250, 100, 50, 30, 15, 10, 5, 3, 1, 0.5]

for i, r in enumerate((UPWARD_COMPUTE, PARALLEL_COMPUTE, DOWNWARD_COMPUTE, 
                       UPWARD_MEMORY, PARALLEL_MEMORY, DOWNWARD_MEMORY, 
                       UPWARD_CONN, PARALLEL_CONN, DOWNWARD_CONN,
                       UPWARD_POWER, PARALLEL_POWER, DOWNWARD_POWER,
                       UPWARD_PRICE, PARALLEL_PRICE, DOWNWARD_PRICE)):
    if len(r) != MAX_POINTS:
        raise Exception(f"Invalid {i}th rubric length. Check configuration.")

def cmc_score(raw: float, rubric: list):
    for i, r in enumerate(rubric):
        if raw <= r:
            return i
    return MAX_POINTS

def pp_score(raw: float, rubric: list):
    for i, r in enumerate(rubric):
        if raw > r:
            return i
    return MAX_POINTS

FLEX_UPWARD = {
    'muldiv':   [2, 1, 0, 0],
    'fpu':      [2, 1, 0, 0],
    'gemm':     [2, 2, 1, 0],
    'crypto':   [1, 1, 1, 0],
    'venc':     [1, 1, 1, 0],
    'vec':      [1, 1, 1, 0],
    'graphics': [1, 1, 1, 0],
}

FLEX_PARALLEL = {
    'muldiv':   [2, 1, 0, 0],
    'fpu':      [2, 1, 0, 0],
    'gemm':     [1, 1, 1, 0],
    'crypto':   [1, 1, 1, 0],
    'vdec':     [1, 1, 1, 0],
    'venc':     [1, 1, 1, 0],
    'isp':      [1, 1, 0, 0],
    'graphics': [1, 1, 1, 0],
}

FLEX_DOWNWARD = {
    'muldiv':   [2, 1, 0, 0],
    'fpu':      [1, 1, 0, 0],
    'gemm':     [1, 1, 1, 0],
    'crypto':   [1, 1, 1, 0],
    'venc':     [1, 1, 1, 0],
    'isp':      [1, 1, 0, 0],
    'vec':      [1, 0, 0, 0],
    'adc':      [1, 1, 1, 0],
    'dac':      [1, 1, 1, 0],
}

def flex_score(specs: dict, rubric: dict):
    score = 0
    for k, v in specs.items():
        if k in rubric.keys():
            score += rubric[k][3-v]
    return score
    
def dev_embedded(specs: dict):
    return specs['isa'] + specs['document'] + specs['toolchain'] + specs['rtos'] + specs['debug']

    
def dev_pu(specs: dict):
    return specs['isa'] + specs['document'] + specs['toolchain'] + specs['os'] + specs['debug']