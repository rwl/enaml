from datetime import datetime
from time import asctime

from enaml.item_models.abstract_item_model import AbstractTableModel
from enaml.styling.brush import Brush
from enaml.styling.color import Color


BRUSH_MAP = {
    'option': Brush(Color.from_string('lightsteelblue'), None),
    'forward': Brush(Color.from_string('paleturquoise'), None),
    'swap': Brush(Color.from_string('khaki'), None),
    'future': Brush(Color.from_string('white'), None),
}


def format_price(price):
    return '%.2f' % price


def format_timestamp(timestamp):
    tt = datetime.fromtimestamp(timestamp).timetuple()
    return asctime(tt)


class TradeTable(AbstractTableModel):

    def __init__(self, book):
        self._book = book
        self._formatters = {'Price': format_price, 'Entry Time': format_timestamp}

    def _get_book(self):
        return self._book
    
    def _set_book(self, book):
        self.begin_reset_model()
        self._book = book
        self.end_reset_model()
    
    book = property(_get_book, _set_book)

    def column_count(self, parent=None):
        if parent is not None:
            return 0
        return len(self._book.fields)
    
    def row_count(self, parent=None):
        if parent is not None:
            return 0
        return len(self._book)
    
    def data(self, index):
        book = self._book
        row = index.row
        col = index.column
        field = book.fields[col]
        fmt = self._formatters.get(field, str)
        val = book[row][field]
        return fmt(val)
    
    def horizontal_header_data(self, section):
        return self._book.fields[section]

    def background(self, index):
        row = index.row
        inst = self._book[row]['Instrument']
        return BRUSH_MAP[inst]


LIME_GREEN = Brush(Color.from_string('limegreen'), None)


class ReportTableModel(AbstractTableModel):

    columns = ['Comment', 'Report', 'Priceable', 'Date', 'Last Event',
               'Market State', 'User', 'Created', 'Updated', 'Status', 'Tag']

    def column_count(self, parent=None):
        if parent is not None:
            return len(self.columns)
        return 0
    
    def row_count(self, parent=None):
        if parent is not None:
            return 100
        return 0
    
    def data(self, index):
        return str(index.row)
    
    def background(self, index):
        return LIME_GREEN

