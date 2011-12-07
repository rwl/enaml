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

from ...styling.style_sheet import StyleSheet, style


#-------------------------------------------------------------------------------
# Default Muntjac style sheet definition
#-------------------------------------------------------------------------------
MUNTJAC_STYLE_SHEET = StyleSheet(

    #---------------------------------------------------------------------------
    # Default style
    #---------------------------------------------------------------------------
    #style("*",
    #    size_policy = "expanding",
    #),

    #---------------------------------------------------------------------------
    # default type overrides
    #---------------------------------------------------------------------------
    #style("PushButton", "CheckBox", "SpinBox", "ComboBox",
    #    size_policy = "preferre",
    #),

    #style("SpinBox", "ComboBox", "Slider", "Panel", "LineEdit", "Field", "Label",
    #    stretch = 1,
    #),

    #style("Html", "Spacer",
    #    stretch = 2,
    #),

    #style("Group", "VGroup", "HGroup",
    #    spacing = 2,
    #),

    style("TableView",
        stretch = 1,
    ),

    #---------------------------------------------------------------------------
    # Convienence style classes
    #---------------------------------------------------------------------------
    style(".error_colors",
        background_color = "error",
        color = "nocolor",
    ),

    style(".normal_colors",
        background_color = "nocolor",
        color = "nocolor",
    ),

    style(".fixed",
        size_policy = "minimum",
    ),

    style(".expanding",
        size_policy = "expanding",
    ),

    style(".no_stretch",
        stretch = 0,
    ),

    style(".stretch",
        stretch = 1,
    ),

    style(".x_stretch",
        stretch = 2,
    ),

    style(".xx_stretch",
        stretch = 3,
    ),

    style(".X_stretch",
        stretch = 4,
    ),

    style(".XX_stretch",
        stretch = 5,
    ),

    style(".no_padding",
        padding = 0,
    ),

    style(".padding",
        padding = 2,
    ),

    style(".x_padding",
        padding = 5,
    ),

    style(".xx_padding",
        padding = 10,
    ),

    style(".X_padding",
        padding = 20,
    ),

    style(".XX_padding",
        padding = 40,
    ),

)
