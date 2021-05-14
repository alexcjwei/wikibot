from Wikibot import Wikibot
from time import time

def main():
  w = Wikibot()
  while (True):
    start = input('Start title: ')
    end = input('Goal title: ')
    w.set_game(start, end)

    begin = time()
    w.run()
    done = time()

    print(f'Search time: {done - begin}')
    print(f'Shortest path: {w.get_path()}')


if __name__ == '__main__':
    main()