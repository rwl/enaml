import enaml

with enaml.imports():
    from trade_viewer import MainWindow

from view_model import ViewModel


view = MainWindow(ViewModel())

view.show()

