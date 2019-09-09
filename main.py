import sys

db = open('./extensions.txt')

targetFile = sys.argv[1]
target = open(targetFile, 'rb')

data = list(i.split('\\') for i in db.readlines())

sample = target.read(100)  # max length of file signature
                           # MSC
                           # MMC Snap-in Control file
                           # 3C3F786D6C2076657273696F6E3D22312E30223F3E0D0A3C4D4D435F436F6E736F6C6546696C6520436F6E736F6C65566572
sampleLength = len(sample)

