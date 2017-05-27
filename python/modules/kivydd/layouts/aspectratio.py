# The code in this file was taken from Stackoverflow
# https://stackoverflow.com/questions/28712359/how-to-fix-aspect-ratio-of-a-kivy-game
#
# Thus the copyright belongs to the user "tito"

from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty

class AspectRatioLayout(RelativeLayout):
  # maximize the children given the ratio
  ratio = NumericProperty(10 / 9.)

  def do_layout(self, *args):
    for child in self.children:
      self.apply_ratio(child)
    super().do_layout()

  def apply_ratio(self, child):
    # ensure the child don't have specification we don't want
    child.size_hint = None, None
    child.pos_hint = {"center_x": .5, "center_y": .5}

    # calculate the new size, ensure one axis doesn't go out of the bounds
    w, h = self.size
    h2 = w * self.ratio
    if h2 > self.height:
      w = h / self.ratio
    else:
      h = h2
    child.size = w, h