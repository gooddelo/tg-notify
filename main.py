import bot
import api
from multiprocessing import Process

def main():
    Process(target=bot.start).start()
    Process(target=api.start).start()

if __name__ == '__main__':
    main()
