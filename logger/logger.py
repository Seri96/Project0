import logging


def log():
    logging.basicConfig(filename="logger.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')


def _test():
    log()


if __name__ == '__main__':
    _test()
