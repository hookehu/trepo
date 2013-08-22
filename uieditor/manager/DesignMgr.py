#-*- coding:utf-8 -*-
'''
The MIT License (MIT)

Copyright(C) 2013 <Hooke HU>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import os
import wx

class DsgnMgr():
		def __init__(self, app):
				self.app = app
				self.app.dsgn.Bind(wx.EVT_MOTION, self.Motion)
				self.selected = None
				self.selectX = 0
				self.selectY = 0
				
		def Motion(self, event):
				if not self.selected:
						return
				p = event.GetPosition()
				p = (p[0] - self.selectX, p[1] - self.selectY)
				self.selected.SetPosition(p)
				
				
		def AddCmp(self, cmpname, x, y):
				localx = x - self.app.dsgn.GetPositionTuple()[0]
				localy = y - self.app.dsgn.GetPositionTuple()[1]
				if cmpname == "Button":
						btn = wx.Button(self.app.dsgn, id = -1, label = cmpname, pos = (localx, localy))
						btn.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						btn.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "Canvas":
						p = wx.Panel(self.app.dsgn, id = -1, pos = (localx, localy))
						p.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						p.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "CheckBox":
						cb = wx.CheckBox(self.app.dsgn, id = -1, label = cmpname, pos = (localx, localy))
						cb.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						cb.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "RadioButton":
						rb = wx.RadioButton(self.app.dsgn, id = -1, label = cmpname, pos = (localx, localy))
						rb.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						rb.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "Panel":
						p = wx.Button(self.app.dsgn, id = -1, label = cmpname, pos = (localx, localy))
						p.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						p.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "Image":
						wx.Button(self.app.dsgn, id = -1, label = cmpname, pos = (localx, localy))
				elif cmpname == "List":
						l = wx.ListCtrl(self.app.dsgn, id = -1, pos = (localx, localy))
						l.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						l.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "TextArea":
						t = wx.TextCtrl(self.app.dsgn, id = -1, pos = (localx, localy))
						t.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						t.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "TextLine":
						t = wx.TextCtrl(self.app.dsgn, id = -1, pos = (localx, localy))
						t.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						t.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "TextInput":
						t = wx.TextCtrl(self.app.dsgn, id = -1, pos = (localx, localy))
						t.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						t.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "Slider":
						s = wx.Slider(self.app.dsgn, id = -1, pos = (localx, localy))
						s.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						s.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "ScrollBar":
						s = wx.ScrollBar(self.app.dsgn, id = -1, pos = (localx, localy))
						s.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						s.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "Label":
						l = wx.Button(self.app.dsgn, id = -1, label = cmpname, pos = (localx, localy))
						l.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						l.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				elif cmpname == "ComboBox":
						cb = wx.ComboBox(self.app.dsgn, id = -1, pos = (localx, localy))
						cb.Bind(wx.EVT_LEFT_DOWN, self.LeftDown)
						cb.Bind(wx.EVT_LEFT_UP, self.LeftUp)
				else:
						print "no support cmp"
						
		def LeftDown(self, event):
				self.selected = event.GetEventObject()
				self.selectX = event.m_x
				self.selectY = event.m_y
				self.selected.SetWindowStyle(wx.RAISED_BORDER)
				
		def LeftUp(self, event):
				self.selected = None