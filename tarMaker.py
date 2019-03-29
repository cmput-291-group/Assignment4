import tarfile

with tarfile.open('A4code.tar.gz','w:gz') as tar:
    tar.add('source.py')
    tar.add('A4README.txt')
    tar.add('A4Report.pdf')