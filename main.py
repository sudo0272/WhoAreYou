import sys
from urllib.request import urlopen
from urllib.error import *
from bs4 import BeautifulSoup

try:
    targetFile = sys.argv[1]
except IndexError:  # no arguments got
    print('Target file has not specified')
    sys.exit()

try:
    db = open('./extensions.txt')
except FileNotFoundError:
    print('extensions.txt not found')
    print('Crawling data')
    try:
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
    except URLError:
        print('Internet not connected')
        sys.exit()

try:
    target = open(targetFile, 'rb')
except FileNotFoundError:
    print(targetFile + ' not found')
    sys.exit()

data = []
for i in db.readlines():
    t = i.split('\\')
    t[2] = t[2].rstrip()

    data.append(t)

sample = target.read(50).hex()  # max length of file signature
                                # MSC
                                # MMC Snap-in Control file
                                # 3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C4D4D435F436F6E736F6C6546696C6520436F6E736F6C65566572
sampleLength = len(sample)

candidates = []

for i in range(len(data)):
    signatureLength = len(data[i][1])
    
    if signatureLength <= sampleLength:
        for j in range(signatureLength):
            if data[i][1][j] != sample[j]:
                break
        
        if j == signatureLength - 1:  # if first part is same
            candidates.append(i)

if len(candidates) != 0:  # if no candidates found
    maxLengthCandidateIndex = candidates[0]

    for i in candidates:
        if len(data[i][1]) > len(data[maxLengthCandidateIndex][1]):
            maxLengthCandidateIndex = i

    maxLengthCandidates = []
    maxLengthCandidateLength = len(data[maxLengthCandidateIndex][1])
    for i in candidates:
        if len(data[i][1]) == maxLengthCandidateLength:
            maxLengthCandidates.append(i)


    print(targetFile, 'can be:')
    for i in maxLengthCandidates:
        print('  ', data[i][0])
        print('    ', data[i][1])
        print('    ', data[i][2])  # don't need '\n' because data[i][2] wasn't stripped

else:
    print(targetFile, '\'s extension was not found')
