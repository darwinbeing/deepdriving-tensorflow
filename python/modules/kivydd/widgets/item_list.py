# The MIT license:
#
# Copyright 2017 Andre Netzeband
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated 
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and 
# to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of 
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO 
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
# SOFTWARE.
#
# Note: The DeepDriving project on this repository is derived from the DeepDriving project devloped by the princeton 
# university (http://deepdriving.cs.princeton.edu/). The above license only applies to the parts of the code, which 
# were not a derivative of the original DeepDriving project. For the derived parts, the original license and 
# copyright is still valid. Keep this in mind, when using code from this project.

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, ListProperty, ColorProperty, NumericProperty, StringProperty
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivydd.app import Widget
from kivy.uix.splitter import Splitter

Builder.load_string("""

<ItemLabel>:
    canvas.before:
        Color:
            rgba: self._BackgroundColor

        Rectangle:
            pos: self.pos
            size: self.size
                        
    canvas.after:
        Color:
            rgba: self._BorderColor
        Line:
            rectangle: self.x+1,self.y+1,self.width-1,self.height-1
        Color:
            rgba: 1, 1, 1, 1


<ItemHeader>
    canvas.before:
        Color:
            rgba: self._BackgroundColor

        Rectangle:
            pos: self.pos
            size: self.size
                        
    canvas.after:
        Color:
            rgba: self._BorderColor
        Line:
            rectangle: self.x+1,self.y+1,self.width-1,self.height-1
        Color:
            rgba: 1, 1, 1, 1

    Button:
        size: root.size
        pos:  root.pos
        text:  self.parent._Text
        color: self.parent._TextColor
        on_press: self.parent._onClick()


<SelectableItem>:
    canvas.before:
        Color:
            rgba: self._SelectedColor if self._IsSelected else self._BackgroundColor

        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        id: Layout
        orientation: "horizontal"
        size: root.size
        pos: root.pos


<ItemListView>:
    viewclass: 'SelectableItem'
    bar_width: 20
    scroll_type: ['bars', 'content']
    bar_color: [0.24, 0.69, 0.85, 1]
    bar_inactive_color: [0.24, 0.69, 0.85, 1]
    
    canvas.before:
        Color:
            rgba: self._BackgroundColor

        Rectangle:
            pos: self.pos
            size: self.size

    SelectableRecycleBoxLayout:
        default_size: None, dp(self.parent._ItemHeight)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'


<ItemList>:   
    BoxLayout:
        orientation: "vertical"
        size: root.size
        pos: root.pos
        
        BoxLayout:
            id: Layout
            orientation: "horizontal"
            size: 1, self.parent.parent._ItemHeight
            size_hint: 1, None
                        
        ItemListView:
            _ItemHeight:      self.parent.parent._ItemHeight
            _Data:            self.parent.parent._Data
            _Sizes:           self.parent.parent._Sizes        
            _BackgroundColor: self.parent.parent._BackgroundColor
            

""")

class ItemLabel(Label):
  _BorderColor     = ColorProperty([0.6, 0.6, 0.6, 1])
  _BackgroundColor = ColorProperty([0.5, 0.5, 0.5, 1])


class ItemHeader(Widget):
  _BorderColor     = ColorProperty([0.6, 0.6, 0.6, 1])
  _BackgroundColor = ColorProperty([0.5, 0.5, 0.5, 1])
  _Text            = StringProperty("")
  _TextColor       = ColorProperty([1, 1, 1, 1])
  _Index           = None
  _onClickFunction = None

  def _onClick(self):
    if self._onClickFunction is not None:
      self._onClickFunction(self, self._Index, self._Text)


class SelectableItem(RecycleDataViewBehavior, Widget):
  _Index           = None
  _IsSelected      = BooleanProperty(False)
  _IsSelectable    = BooleanProperty(True)
  _Data            = ListProperty([])
  _Sizes           = ListProperty([])
  _TextColor       = ColorProperty([0, 0, 0, 1])
  _BackgroundColor = ColorProperty([0.75, 0.75, 0.75, 1])
  _SelectedColor   = ColorProperty([0.44, 0.77, 0.89, 1])


  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.bind(_Data      = self.onDataChange)
    self.bind(_TextColor = self.onDataChange)
    self.bind(_Sizes     = self.onDataChange)


  def onDataChange(self, Instance, Columns):
    self.ids.Layout.clear_widgets()

    for i, Column in enumerate(self._Data):
      NewLabel = ItemLabel(text=str(Column))
      NewLabel.color = self._TextColor
      NewLabel._BackgroundColor = [0, 0, 0, 0]

      if len(self._Sizes) > i:
        if self._Sizes[i] is not None:
          NewLabel.size_hint = (None, 1)
          NewLabel.size      = (self._Sizes[i], 1)

      self.ids.Layout.add_widget(NewLabel)


  def refresh_view_attrs(self, rv, index, data):
    ''' Catch and handle the view changes '''
    self._Index = index
    return super().refresh_view_attrs(rv, index, data)


  def on_touch_down(self, touch):
    ''' Add selection on touch down '''
    if super().on_touch_down(touch):
      return True
    if self.collide_point(*touch.pos) and self._IsSelectable:
      return self.parent.select_with_touch(self._Index, touch)


  def apply_selection(self, rv, index, is_selected):
    ''' Respond to the selection of items in the view. '''
    self._IsSelected = is_selected
    #if is_selected:
    #  print("selection changed to {0}".format(rv.data[index]))
    #else:
    #  print("selection removed for {0}".format(rv.data[index]))


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
  pass


class ItemListView(RecycleView):
  _ItemHeight      = NumericProperty(30)
  _Sizes           = ListProperty([])
  _Data            = ListProperty([])
  _BackgroundColor = ColorProperty([1, 1, 1, 1])

  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.bind(_Data=self._onDataChange)
    self.bind(_Sizes=self._onDataChange)

  def _onDataChange(self, Instance, Value):
    List = [{'_BackgroundColor': self._BackgroundColor, '_Sizes': self._Sizes, '_Data': Date} for Date in self._Data]
    self.data = List


class ItemList(Widget):
  _Header          = ListProperty([])
  _ItemHeight      = NumericProperty(30)
  _HeaderTextColor = ColorProperty([1, 1, 1, 1])
  _BackgroundColor = ColorProperty([0.75, 0.75, 0.75, 1])
  _Sizes           = ListProperty([])
  _Data            = ListProperty([])
  _UpdateFunc      = None


  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.bind(_Header          = self._onHeaderChange)
    self.bind(_HeaderTextColor = self._onHeaderChange)
    self.bind(_Sizes           = self._onHeaderChange)
    MyApp = App.get_running_app()
    MyApp.registerUpdateFunc(self, self.updateList)


  def __del__(self):
    self._UpdateFunc = None


  def updateList(self, *args):
    if self._UpdateFunc != None:
      self._Data = self._UpdateFunc()


  def _onHeaderChange(self, Instance, Value):
    self.ids.Layout.clear_widgets()

    for i, Column in enumerate(self._Header):
      NewLabel                  = ItemHeader()
      NewLabel._Text            = Column
      NewLabel._TextColor       = self._HeaderTextColor
      NewLabel._Index           = i
      NewLabel._onClickFunction = self._onHeaderClick

      if len(self._Sizes) > i:
        if self._Sizes[i] is not None:
          NewLabel.size_hint = (None, 1)
          NewLabel.size      = (self._Sizes[i], 1)

      self.ids.Layout.add_widget(NewLabel)


  def _onHeaderClick(self, Instance, Index, Text):
    print("Click on Header \"{}\" ({}).".format(Text, Index))