from urllib.request import urlopen
from bs4 import BeautifulSoup

signatures = []

db = open('extensions.txt', 'w')

for i in range(1, 19):
    url = 'https://filesignatures.net/index.php?page=all&order=EXT&alpha=&currentpage=%d' % i

    webpage = urlopen(url)

    source = BeautifulSoup(webpage, 'html5lib').find('table', {'id': 'innerTable'}).find('tbody')

    for i in source.findChildren('tr'):
        t = list(j.get_text().strip() for j in i.findChildren('td'))

        t.pop(0)

        if t[0] != 'Extension':
            t[1] = ''.join(t[1].split(' '))
            
            db.write('\\'.join(t))
            db.write('\n')

db.close()
