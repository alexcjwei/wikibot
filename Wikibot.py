from Node import Node
import requests
from bs4 import BeautifulSoup
import queue
 
class Wikibot:
  url = 'https://en.wikipedia.org/wiki/'
  api = 'https://en.wikipedia.org/w/api.php'
  path_start = 30
  wiki_start = 6
  params = {'action': 'query',
                    'format': 'json',
                    'prop': 'linkshere',
                    'lhlimit': 'max'}

  def __init__(self, start, end, search_type='BFS', bidirectional=False, ):
    # self.start = start[Wikibot.path_start:]
    # self.end = end[Wikibot.path_start:]
    self.start = end.lower()
    self.end = start.lower()
    self.type = search_type
    self.session = requests.Session()

    self.queue = [Node(None, self.start)]
    self.params = {'action': 'query',
                    'format': 'json',
                    'prop': 'linkshere',
                    'lhlimit': 'max'}

    self.discovered = dict()

    self.found = None

  def __init__(self, search_type='BFS'):
    self.type = search_type
    self.session = requests.Session()
    self.params = {'action': 'query',
                    'format': 'json',
                    'prop': 'linkshere',
                    'lhlimit': 'max'}

  def set_game(self, start, end):
    self.start = end.lower()
    self.end = start.lower()
    self.queue = [Node(None, self.start)]
    self.discovered = dict()
    self.found = None

  def BFS(self):
    while self.queue and not self.found:
      cur  = self.queue.pop(0)
      if cur.get_name() == self.end:
        return cur
      self.grow(cur)
      print(cur.get_path())
      for child in cur.get_children(): # children not discovered by default
        name = child.get_name()
        if name == self.end:
            return child
        elif name not in self.discovered:
          self.discovered[name] = child
          self.queue.append(child)


  # in: cur --> next --> next.get_parent() --> None

  # ... <-- cur --> next --> None
  def reverse(self, node):
    cur = node
    next = cur.get_parent()
    while next and next.get_parent():
      temp = next.get_parent()
      next.set_parent(cur)
      cur = next
      next = temp
    next.set_parent(cur)
    return next


  def biBFS(self): # DOES NOT WORK AS INTENDED (links are not bidirectional)
    self.end_queue = [Node(None, self.end)]
    self.end_discovered = dict()
    up = 1
    while (self.queue or self.end_queue) and not self.found:
      queue = self.queue if up else self.end_queue
      discovered = self.discovered if up else self.end_discovered
      end_discovered = self.end_discovered if up else self.discovered

      length = len(queue)
      while length > 0: # go through each originally in queue
        self.found = self.bisearch(queue, discovered, end_discovered)
        if self.found:
          return self.found
        length -= 1
      up = not up

  def bisearch(self, queue, discovered, end_discovered): 
    cur  = queue.pop(0)
    print(cur.get_path())
    self.grow(cur)
    for child in cur.get_children(): # children not discovered by default
      name = child.get_name()
      if name == 'action film':
        print(f'Parent: {cur.get_name()}, Child: {name}')
      if discovered == self.discovered and name == self.end:
        print('--- Found from the start!')
        return child # grew down to child (worry about flipping later)
      elif discovered == self.end_discovered and name == self.start:
        print('---- Found from the end!')
        return self.reverse(child)
      elif name in end_discovered: # found in opposite direction: connect and reverse lineage of other node
        print('----Met in the middle!')
        tail = self.reverse(child)
        parent = end_discovered[name].get_parent()
        child.set_parent(parent)
        return tail
      elif name not in discovered:
        discovered[name] = child
        queue.append(child)
    return None

  def grow(self, node):
    for title in self.load_page(node):
      child = Node(node, title.lower())
      node.add_child(child)


  def run(self):
    if self.type == 'BFS':
      self.found = self.BFS()
    elif self.type == 'IDDFS':
      self.BFS()
    elif self.type == 'biBFS':
      self.found = self.biBFS()

  def load_page(self, node):
    self.params['titles'] = node.get_name()
    titles = []
    res = self.session.get(url=Wikibot.api, params=self.params)
    data = res.json()
    pages = data['query'].get('pages') if data.get('query') else None
    if pages:
      for key, val in pages.items():
        links = val.get('linkshere')
        if links:
          for link in links:
            titles.append(link.get('title'))
    return titles


  def get_path(self):
    if not self.found:
      print('Path not yet found')
      return
    return self.found.get_path()

