from arknights.agent import Agent
import argparse
import numpy as np
import sys


parser = argparse.ArgumentParser()
parser.add_argument('-r', '--resolution', type=str, default='1600,900')
parser.add_argument('-l', '--local-host', type=str, default='127.0.0.1:7555')
parser.add_argument('-t', '--tessdata-dir', type=str, default=None)
parser.add_argument('-m', '--missions', type=str, default=None)
parser.add_argument('--daily', '-d', type=int, default=None, help='do daily `n` times')
parser.add_argument('--use-mixture', default=False, action='store_true')
parser.add_argument('--use-stone', default=False, action='store_true')
parser.add_argument('--n-mixture', type=int, default=None)
parser.add_argument('--n-stone', type=int, default=None)
parser.add_argument('--plan', '-p', type=str, default=None, help='a cmd statement executed after missions are completed')
args = parser.parse_args()

def main():
    resolution = [int(i) for i in args.resolution.split(',')]

    local_host = args.local_host

    tessdata_dir = args.tessdata_dir

    use_mixture = args.use_mixture
    use_stone = args.use_stone
    n_mixture = args.n_mixture
    n_stone = args.n_stone
    plan = args.plan
    daily = args.daily

    try:
        missions = args.missions.split(',')
        missions = dict(np.reshape(missions, [-1, 2]))
    except:
        raise Exception('`-m/--missions` expect format `mission_name,times[,mission_name,times[...`\
                        for examples:\nmain.py -m CE-5,5')

    for k, v in missions.items():
        missions[k] = int(v)

    agent = Agent(missions,
                  resolution=resolution,
                  local_host=local_host,
                  tessdata_dir=tessdata_dir,
                  use_mixture=use_mixture,
                  use_stone=use_stone,
                  n_stone=n_stone,
                  n_mixture=n_mixture,
                  plan=plan,
                  daily=daily)

    agent._run()


if __name__ == '__main__':
    main()