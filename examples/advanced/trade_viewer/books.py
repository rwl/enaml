

class Book(object):

    def __init__(self, trades):
        self._trades = trades

    def __len__(self):
        return len(self._trades)

    def __getitem__(self, idx):
        return self._trades[idx]
    
    @property
    def fields(self):
        return self._trades.dtype.names
    

def load_trades():
    import numpy as np
    import generate_data
    mm = np.memmap('./trades.arr', mode='r')
    trades = mm.view(generate_data.trade_dt)
    return trades


_trades = load_trades()


BOOKS = {
    'ALL': Book(_trades),
    'FOO': Book(_trades[:2500000]),
    'BAR': Book(_trades[2500000:5000000]),
    'BAZ': Book(_trades[5000000:7500000]),
    'HAM': Book(_trades[7500000:]),
}

