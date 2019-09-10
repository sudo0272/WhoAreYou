import sys

try:
    targetFile = sys.argv[1]
except IndexError:  # no arguments got
    print('Target file has not specified')
    sys.exit()

try:
    db = open('./extensions.txt')
except FileNotFoundError:
    print('extensions.txt not found')
    sys.exit()

try:
    target = open(targetFile, 'rb')
except FileNotFoundError:
    print(targetFile + ' not found')
    sys.exit()

data = list(i.split('\\') for i in db.readlines())

# print(data)

sample = target.read(50).hex()  # max length of file signature
                                # MSC
                                # MMC Snap-in Control file
                                # 3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C4D4D435F436F6E736F6C6546696C6520436F6E736F6C65566572
sampleLength = len(sample)

# print(sample)

candidates = []

for i in range(len(data)):  # remove *
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
