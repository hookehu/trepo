#-*- coding:utf-8 -*-
'''
The MIT License (MIT)

Copyright(C) 2013 <Hooke HU>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import wx

class DisplayObject(object):
		def __init__(self):
				self.x = 0
				self.y = 0
				self.width = 0
				self.height = 0
				
class Button(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				self.upSkin = None
				self.overSkin = None
				self.downSkin = None
				
class Canvas(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				self.bg = None
				
class CheckBox(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				self.selectSkin = None
				
class RadioButton(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				self.selectSkin = None
				
class Panel(Canvas):
		def __init__(self):
				Canvas.__init__(self)
				self.title = None
				
class Image(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				self.source = None
				
class ListView(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				self.cellRenderer = None
				self.rowHeight = 0
				self.bg = None
				
class TextArea(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				self.bg = None
				
class TextLine(TextArea):
		def __init__(self):
				TextArea.__init__(self)
				
class TextInput(TextArea):
		def __init__(self):
				TextArea.__init__(self)
				self.password = False
				
class Slider(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				self.btn = None
				self.line = None
				
class ScrollBar(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				self.upBtn = None
				self.downBtn = None
				self.trackBtn = None
				self.trackBg = None
				
class Label(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				
class ComboBox(DisplayObject):
		def __init__(self):
				DisplayObject.__init__(self)
				
