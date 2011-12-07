#------------------------------------------------------------------------------
# Copyright (C) 2011 Enthought, Inc.
# Copyright (C) 2011 Richard Lincoln
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#------------------------------------------------------------------------------

from ...toolkit import Constructor


def importer(module_path, name):
    def _importer():
        mod = __import__(module_path, fromlist=[name])
        try:
            res = getattr(mod, name)
        except AttributeError:
            raise ImportError('Cannot import name %s' % name)
        return res
    return _importer


def constructor(base_path):
    """ A factory function which understands our name mangling and will
    create a constructor instance. Returns tuple of (name, ctor) where
    name is a string that can be used by toolkit to refer to the ctor
    in the enaml source code.

    """
    c_module_path = 'enaml.widgets.' + base_path
    c_name = ''.join(part.capitalize() for part in base_path.split('_'))

    t_module_path = 'enaml.widgets.muntjac.' + 'muntjac_' + base_path
    t_name = 'Muntjac' + c_name

    shell_loader = importer(c_module_path, c_name)
    abstract_loader = importer(t_module_path, t_name)

    ctor = Constructor(shell_loader, abstract_loader)

    return c_name, ctor


MUNTJAC_CONSTRUCTORS = dict((
    constructor('window'),
    constructor('component'),
    constructor('container'),
    constructor('dialog'),
    constructor('calendar'),
    constructor('check_box'),
    constructor('combo_box'),
    constructor('field'),
    constructor('html'),
    constructor('image'),
    constructor('label'),
    constructor('push_button'),
    constructor('radio_button'),
    constructor('slider'),
    constructor('spin_box'),
    constructor('traitsui_item'),
    constructor('enable_canvas'),
    constructor('list_view'),
    constructor('table_view'),
    constructor('tree_view'),
    constructor('date_edit'),
    constructor('datetime_edit'),
    constructor('form'),
    constructor('group_box'),
    constructor('stacked'),
    constructor('scroll_area'),
    constructor('progress_bar'),
    constructor('tabbed'),
    constructor('tab'),
    constructor('splitter'),
))

