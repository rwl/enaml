from traits.api import HasTraits, Instance, Str, Property, Dict

from books import BOOKS
from trade_table_model import TradeTable


class EventsModel(HasTraits):

    trade_table = Instance(TradeTable)

    _books = Dict(BOOKS)

    book_choices = Property(depends_on='_books')

    book_choice = Str('ALL')

    def _trade_table_default(self):
        book = self._books[self.book_choice]
        return TradeTable(book)
    
    def _get_book_choices(self):
        return sorted(self._books.keys())
    
    def _book_choice_changed(self, choice):
        book = self._books[choice]
        self.trade_table.book =  book


class MarketDataModel(HasTraits):
    pass

    
class ViewModel(HasTraits):

    events_model = Instance(EventsModel, ())

    market_data_model = Instance(MarketDataModel, ())

