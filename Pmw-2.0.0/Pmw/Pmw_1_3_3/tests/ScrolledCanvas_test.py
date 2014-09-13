import Test
import Pmw

Test.initialise()

c = Pmw.ScrolledCanvas

def _createOvals():
    w = Test.currentWidget()
    w.create_oval(50, 50, 150, 100, fill = 'red')
    w.create_oval(100, 50, 150, 150, fill = 'blue')
    w.create_oval(50, 100, 200, 350, fill = 'yellow')

def _createWindow():
    w = Test.currentWidget()
    lb = Pmw.ScrolledListBox(w.interior(),
	    items = range(20), listbox_height = 6)
    w.create_window(300, 100, window = lb)

def _testYView(doBottom):
    w = Test.currentWidget()
    top, bottom = w.yview()
    if type(top) != type(0.0) or type(bottom) != type(0.0):
        return 'bad type ' + str(top) + ' ' + str(bottom)
    if doBottom:
        if bottom != 1.0:
            return 'bottom is ' + str(bottom)
    else:
        if top != 0.0:
            return 'top is ' + str(top)

kw_1 = {'labelpos': 'n', 'label_text': 'ScrolledCanvas', 'borderframe' : 1}
tests_1 = (
  (c.pack, (), {'padx' : 10, 'pady' : 10, 'fill' : 'both', 'expand' : 1}),
  (Test.num_options, (), 8),
  (_createOvals, ()),
  (c.resizescrollregion, ()),
  (_createWindow, ()),
  (c.resizescrollregion, ()),
  ('hull_background', 'aliceblue'),
  ('Scrollbar_borderwidth', 3),
  ('hull_cursor', 'gumby'),
  ('label_text', 'Label'),
  ('Scrollbar_repeatdelay', 200),
  ('Scrollbar_repeatinterval', 105),
  ('vscrollmode', 'none'),
  ('vscrollmode', 'static'),
  ('vscrollmode', 'dynamic'),
  ('hscrollmode', 'none'),
  ('hscrollmode', 'static'),
  ('hscrollmode', 'dynamic'),
  ('Scrollbar_width', 20),
  ('vscrollmode', 'bogus', 'ValueError: bad vscrollmode ' +
    'option "bogus": should be static, dynamic, or none'),
  ('hscrollmode', 'bogus', 'ValueError: bad hscrollmode ' +
    'option "bogus": should be static, dynamic, or none'),
  (c.yview, ('moveto', 0.0)),
  (_testYView, 0),
  (c.yview, ('moveto', 0.02)),
  (c.yview, ('moveto', 0.04)),
  (c.yview, ('moveto', 0.06)),
  (c.yview, ('moveto', 0.08)),
  (c.yview, ('moveto', 0.10)),
  (c.yview, ('moveto', 0.12)),
  (c.yview, ('moveto', 0.14)),
  (c.yview, ('moveto', 0.16)),
  (c.yview, ('moveto', 0.18)),
  (c.yview, ('moveto', 0.20)),
  (c.yview, ('moveto', 0.22)),
  (c.yview, ('moveto', 0.24)),
  (c.yview, ('moveto', 0.26)),
  (c.yview, ('moveto', 0.28)),
  (c.yview, ('moveto', 0.98)),
  (_testYView, 1),
  (c.yview, ('scroll', -1, 'page')),
  (c.yview, ('scroll', -1, 'page')),
  (_testYView, 0),
  (c.yview, ('scroll', 1, 'page')),
  (c.yview, ('scroll', 1, 'page')),
  (_testYView, 1),
)

kw_2 = {
  'hscrollmode' : 'dynamic',
  'label_text' : 'Label',
  'labelpos' : 'n',
  'scrollmargin': 20,
  'canvasmargin': 20,
  'usehullsize': 1,
  'hull_width' : 500,
  'hull_height' : 200,
}
tests_2 = (
  (c.pack, (), {'padx' : 10, 'pady' : 10, 'fill' : 'both', 'expand' : 1}),
)

alltests = (
  (tests_1, kw_1),
  (tests_2, kw_2),
)

testData = ((Pmw.ScrolledCanvas, alltests),)

if __name__ == '__main__':
    Test.runTests(testData)
