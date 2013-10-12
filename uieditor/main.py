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
import mgrs

class WinApp(wx.App):
		def OnInit(self):
				self.RedirectStdio("error.log")
				self.frame = wx.Frame(parent = None, id = -1, title="uieditor", size = (1000, 768), pos = (0, 0))
				self.InitMenuBar()
				self.InitPanels()
				self.frame.Show()
				self.prj_mgr = mgrs.PrjMgr(self)
				self.cmp_mgr = mgrs.CmpsMgr(self)
				self.dsgn_mgr = mgrs.DsgnMgr(self)
				return True
				
		def InitMenuBar(self):
				bar = wx.MenuBar()
				menu = wx.Menu()
				bar.Append(menu, "File")
				item = wx.MenuItem(parentMenu = menu, id = -1, text = "Open Prj")
				menu.AppendItem(item)
				self.Bind(wx.EVT_MENU, self.OpenPrjHandler, item)
				item = wx.MenuItem(parentMenu = menu, id = -1, text = "New Prj")
				menu.AppendItem(item)
				self.Bind(wx.EVT_MENU, self.NewPrjHandler, item)
				item = wx.MenuItem(parentMenu = menu, id = -1, text = "New File")
				menu.AppendItem(item)
				self.Bind(wx.EVT_MENU, self.NewFileHandler, item)
				item = wx.MenuItem(parentMenu = menu, id = -1, text = "New Folder")
				menu.AppendItem(item)
				self.Bind(wx.EVT_MENU, self.NewFolderHandler, item)
				item = wx.MenuItem(parentMenu = menu, id = -1, text = "Del File")
				menu.AppendItem(item)
				self.Bind(wx.EVT_MENU, self.DelFileHandler, item)
				item = wx.MenuItem(parentMenu = menu, id = -1, text = "Del Folder")
				menu.AppendItem(item)
				self.Bind(wx.EVT_MENU, self.DelFolderHandler, item)
				item = wx.MenuItem(parentMenu = menu, id = -1, text = "Save")
				menu.AppendItem(item)
				self.Bind(wx.EVT_MENU, self.SaveHandler, item)
				item = wx.MenuItem(parentMenu = menu, id = -1, text = "Expose")
				menu.AppendItem(item)
				self.Bind(wx.EVT_MENU, self.ExposeHandler, item)
				item = wx.MenuItem(parentMenu = menu, id = -1, text = "Exit")
				menu.AppendItem(item)
				self.Bind(wx.EVT_MENU, self.ExitHandler, item)
				self.frame.SetMenuBar(bar)
				
		def InitPanels(self):
				self.left = wx.SplitterWindow(self.frame, id = -1, pos = wx.DefaultPosition,
													size = (200, 768), style = wx.SP_3D,
													name = "")
				self.prj = wx.Panel(self.left, style = wx.SUNKEN_BORDER)
				self.cmps = wx.Panel(self.left, style = wx.SUNKEN_BORDER)
				self.left.SplitHorizontally(self.prj, self.cmps)
				
				self.middle = wx.SplitterWindow(self.frame, id = -1, pos = (200, 0),
													size = (600, 768), style = wx.SP_3D,
													name = "")
				self.dsgn = wx.Panel(self.middle, style = wx.SUNKEN_BORDER)
				self.log = wx.Panel(self.middle, style = wx.SUNKEN_BORDER)
				self.middle.SplitHorizontally(self.dsgn, self.log)
				
				self.right = wx.SplitterWindow(self.frame, id = -1, pos = (800, 0),
													size = (200, 768), style = wx.SP_3D,
													name = "")
				self.prop = wx.Panel(self.right, style = wx.SUNKEN_BORDER)
				self.layer = wx.Panel(self.right, style = wx.SUNKEN_BORDER)
				self.right.SplitHorizontally(self.prop, self.layer)
				
				self.prj_tree = wx.TreeCtrl(self.prj)
				self.prj_tree.SetSize(self.prj.GetSize())
				
				self.cmp_tree = wx.TreeCtrl(self.cmps)
				self.cmp_tree.SetSize(self.cmps.GetSize())
				
				self.layer_tree = wx.TreeCtrl(self.layer)
				self.layer_tree.SetSize(self.layer.GetSize())
				
				self.log_area = wx.TextCtrl(self.log, style = wx.TE_MULTILINE | wx.TE_RICH2)
				self.log_area.SetSize(self.log.GetSize())
				
		def NewPrjHandler(self, event):
				dialog = wx.FileDialog(None, "New Prj", os.getcwd(), "", "", wx.SAVE)
				if dialog.ShowModal() != wx.ID_OK:
						return
				self.ShowToLog(dialog.GetPath())
				
		def OpenPrjHandler(self, event):
				dialog = wx.FileDialog(None, "Open Prj", os.getcwd(), "", "", wx.OPEN)
				if dialog.ShowModal() != wx.ID_OK:
						return
				self.prj_mgr.OpenPrjHandler(dialog.GetPath())
				
		def NewFileHandler(self, event):
				pass
				
		def NewFolderHandler(self, event):
				pass
				
		def DelFileHandler(self, event):
				pass
				
		def DelFolderHandler(self, event):
				pass
				
		def SaveHandler(self, event):
				pass
				
		def ExposeHandler(self, event):
				pass
				
		def ExitHandler(self, event):
				pass
				
		def UpdateProp(self, ctrl):
				pass
				
		def Output(self):
				pass
				
		def ShowToLog(self, text):
				self.log_area.AppendText(text)
				
def main():
		app = WinApp()
		app.MainLoop()
		
if __name__ == "__main__":
		main()