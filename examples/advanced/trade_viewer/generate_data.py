import random
import string
import numpy as np


trade_dt = np.dtype([
    ('Trade ID', 'S8'),
    ('Instrument', 'S8'),
    ('Quantity', np.int32),
    ('Pair', 'S8'),
    ('Price', np.float32),
    ('Entry Time', np.int32),
    ('Trader', 'S8'),
])


def gen_trade_id():
    letters = [random.choice(string.ascii_uppercase) for _ in xrange(6)]
    n = random.choice(string.digits)
    return letters[0] + n + '-' + ''.join(letters[1:])


insts = ('option', 'swap', 'forward', 'future')
def gen_instrument():
    return random.choice(insts)


quantities = [int(2e5), int(1e6), int(10e6), int(5e5), int(5e4)]
def gen_quantity():
    return random.choice(quantities)


overs = ['USD', 'GBP', 'CHF', 'YEN']
unders = ['JPY', 'EUR', 'AUD', 'SKK']
def gen_pair():
    over = random.choice(overs)
    under = random.choice(unders)
    return over + '/' + under


def gen_price():
    return random.random() * 150


def gen_entry_time():
    return random.randint(0, 2e9)


def gen_trader():
    l = random.choice(string.ascii_lowercase)
    return l + ''.join(random.choice(string.digits) for _ in xrange(7))


def generate_data():
    # There is a bug in np.memmap on windows where we can't create a memmap
    # using a structured dtype. Instead create one the size we need, then
    # take a view of it using the custom dtype.
    nrecords = int(10e6)

    bytes_per = trade_dt.itemsize

    mm = np.memmap('./trades.arr', mode='w+', shape=(nrecords * bytes_per,))
    mm.flush()

    mm = np.memmap('./trades.arr', mode='r+')
    mv = mm.view(dtype=trade_dt)

    gens = zip(trade_dt.names, (
        gen_trade_id,
        gen_instrument,
        gen_quantity,
        gen_pair,
        gen_price,
        gen_entry_time,
        gen_trader,
    ))

    for idx in xrange(nrecords):
        for field, gen in gens:
            mv[idx][field] = gen()

    mm.flush()


if __name__ == '__main__':
    # Uncomment and run as main to regenerate data. 
    # This will take several minutes.
    # generato_data()
    pass

