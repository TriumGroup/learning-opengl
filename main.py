import sys
import os

from cubes.application import Application

DEFAULT_PATH = 'files'

def main():
    if len(sys.argv) == 2:
        path = sys.argv[1]
        if not os.path.isdir(path):
            print('Invalid directory')
            sys.exit(1)
    else:
        path = DEFAULT_PATH
    app = Application(path)
    app.start()

if __name__ == '__main__':
    main()
