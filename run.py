import os
import json
import math

import numpy as np
from matplotlib import pyplot as plt

from rubrics import *

files = os.listdir('targets')

def parse_size_to_number(val: str):
    if val.endswith('GB'):
        t = val.replace('GB', '')
        return float(t) * GB
    elif val.endswith('Gb'):
        t = val.replace('Gb', '')
        return float(t) * Gb
    elif val.endswith('MB'):
        t = val.replace('MB', '')
        return float(t) * MB
    elif val.endswith('Mb'):
        t = val.replace('Mb', '')
        return float(t) * Mb
    elif val.endswith('KB'):
        t = val.replace('KB', '')
        return float(t) * KB
    elif val.endswith('Kb'):
        t = val.replace('Kb', '')
        return float(t) * Kb
    else:
        return None

def parse_bw_to_number(val: str):
    if val.endswith('GB/s'):
        t = val.replace('GB/s', '')
        return float(t) * GB
    elif val.endswith('Gbps'):
        t = val.replace('Gbps', '')
        return float(t) * Gb
    elif val.endswith('MB/s'):
        t = val.replace('MB/s', '')
        return float(t) * MB
    elif val.endswith('Mbps'):
        t = val.replace('Mbps', '')
        return float(t) * Mb
    elif val.endswith('KB/s'):
        t = val.replace('KB/s', '')
        return float(t) * KB
    elif val.endswith('Kbps'):
        t = val.replace('Kbps', '')
        return float(t) * Kb
    else:
        return None

def draw_radar_graph(values, tags):
    angles = np.linspace(0, 2*math.pi, len(values), endpoint=False).tolist()

    angles += angles[:1]
    values += values[:1]
    tags += tags[:1]

    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_ylim([0,10])

    ax.plot(angles, values, color='red', linewidth=1)
    ax.fill(angles, values, color='red', alpha=0.25)
    ax.set_thetagrids(np.degrees(angles), tags, fontsize=20)

    return fig, ax

for file in files:
    if file.endswith('.json'):
        try:
            obj = json.load(open('targets/' + file))

            raw_compute_score = 0
            for i in obj['compute']:
                if i['type'] == 'coremark':
                    raw_compute_score += i['score']
                elif i['type'] == 'clpeak':
                    raw_compute_score += 350 * math.sqrt((i['int'] + i['float'] + 2 * i['double']) * i['memory'])
            
            raw_memory_score = 0
            for i in obj['memory']:
                size = parse_size_to_number(i['size'])
                bw = parse_bw_to_number(i['bandwidth'])
                raw_memory_score += size * bw
            
            raw_connectivity_score = 0
            for i in obj['connectivity']:
                raw_connectivity_score += parse_bw_to_number(i['bandwidth'])
            
            print(raw_compute_score, raw_memory_score, raw_connectivity_score)

            # Upward.
            compute = cmc_score(raw_compute_score, UPWARD_COMPUTE)
            memory = cmc_score(raw_memory_score, UPWARD_MEMORY)
            connectivity = cmc_score(raw_connectivity_score, UPWARD_CONN)
            power = pp_score(obj['power'], UPWARD_POWER)
            price = pp_score(obj['price'], UPWARD_PRICE)
            flex = flex_score(obj['flex'], FLEX_UPWARD)
            dev = dev_pu(obj['dev'])

            fig, ax = draw_radar_graph(
                [compute, memory, connectivity, power, price, flex, dev],
                ['Compute', "Memory", "Conn", "Power", "Price", "Flex", "Dev"]
            )
            fig.savefig('results/' + obj['name'] + '-upward.png')
            fig.savefig('results/' + obj['name'] + '-upward.pdf')

            # Parallel.
            compute = cmc_score(raw_compute_score, PARALLEL_COMPUTE)
            memory = cmc_score(raw_memory_score, PARALLEL_MEMORY)
            connectivity = cmc_score(raw_connectivity_score, PARALLEL_CONN)
            power = pp_score(obj['power'], PARALLEL_POWER)
            price = pp_score(obj['price'], PARALLEL_PRICE)
            flex = flex_score(obj['flex'], FLEX_PARALLEL)
            dev = dev_pu(obj['dev'])

            fig, ax = draw_radar_graph(
                [compute, memory, connectivity, power, price, flex, dev],
                ['Compute', "Memory", "Conn", "Power", "Price", "Flex", "Dev"]
            )

            print([compute, memory, connectivity, power, price, flex, dev])
            fig.savefig('results/' + obj['name'] + '-parallel.png')
            fig.savefig('results/' + obj['name'] + '-parallel.pdf')

            # Downward.
            compute = cmc_score(raw_compute_score, DOWNWARD_COMPUTE)
            memory = cmc_score(raw_memory_score, DOWNWARD_MEMORY)
            connectivity = cmc_score(raw_connectivity_score, DOWNWARD_CONN)
            power = pp_score(obj['power'], DOWNWARD_POWER)
            price = pp_score(obj['price'], DOWNWARD_PRICE)
            flex = flex_score(obj['flex'], FLEX_DOWNWARD)
            dev = dev_pu(obj['dev'])

            fig, ax = draw_radar_graph(
                [compute, memory, connectivity, power, price, flex, dev],
                ['Compute', "Memory", "Conn", "Power", "Price", "Flex", "Dev"]
            )
            fig.savefig('results/' + obj['name'] + '-downward.png')
            fig.savefig('results/' + obj['name'] + '-downward.pdf')

        except Exception as e:
            print('Error parsing file: ' + file)
            raise e
            continue