from Wikibot import Wikibot
from time import time

def main():
  # start = 'https://en.wikipedia.org/wiki/Die_Hard'
  # end = 'https://en.wikipedia.org/wiki/Gautama_Buddha'
  start = 'die hard'
  # end = 'action film'
  end = 'protagonist'
  # die hard --> action film --> protagonist
  w = Wikibot(start, end, 'biBFS')
  print(f'{start} -> {end}')
  start = time()
  w.run()
  end = time()
  print(f'Search time: {end-start}')
  w.print_path()


  # grow start
  # for each child of start, grow child


if __name__ == '__main__':
    main()