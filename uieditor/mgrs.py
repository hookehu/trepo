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

class PrjMgr():
		def __init__(self, app):
				self.app = app
				self.prj_path = ""
				self.root_name = ""
				
		def ReadPrj(self, prjname):
				pass
				
		def NewPrjHandler(self, prjname):
				pass
				
		def NewFileHandler(self, filename):
				pass
				
		def NewFolderHandler(self, folder):
				pass
				
		def DelFileHandler(self, filename):
				pass
				
		def DelFolderHandler(self, folder):
				pass
				
		def OpenPrjHandler(self, filename):
				self.prj_path = os.path.dirname(filename)
				self.root_name = os.path.basename(filename)
				files = os.listdir(self.prj_path)
				root = TreeNode(self.root_name, True)
				root.isRoot = True
				self.BuildTree(self.prj_path, root)
				self.UpdateTree(None, root)
						
		def BuildTree(self, path, parent):
				files = os.listdir(path)
				for f in files:
						if not os.path.isdir(os.path.join(path, f)):
								node = TreeNode(f, False)
								parent.AddNode(node)
								continue
						node = TreeNode(f, True)
						parent.AddNode(node)
						self.BuildTree(os.path.join(path, f), node)
						
		def UpdateTree(self, parent, node):
				if node.isRoot:
						root = self.app.prj_tree.AddRoot(node.name)
						for n in node.children:
								self.UpdateTree(root, n)
						return
				if node.isFolder:
						p = self.app.prj_tree.AppendItem(parent, node.name)
						for n in node.children:
								self.UpdateTree(p, n)
						return
				self.app.prj_tree.AppendItem(parent, node.name)
				
class TreeNode():
		def __init__(self, name, isFolder):
				self.name = name
				self.open = False
				self.children = []
				self.isFolder = isFolder
				self.isRoot = False
				
		def AddNode(self, node):
				self.children.append(node)
				
		def DelNode(self, node):
				self.children.remove(node)
				
		def DelAllNode(self):
				self.children = []
				
		def Open(self):
				self.Open = True
				
		def Close(self):
				self.Open = False
				
class CmpDropTarget(wx.TextDropTarget):
		def __init__(self, app):
				wx.TextDropTarget.__init__(self)
				self.app = app
				
		def OnDropText(self, x, y, text):
				self.app.dsgn_mgr.AddCmp(text, x, y)
				
class CmpsMgr():
		def __init__(self, app):
				self.app = app
				self.BuildTree()
				self.UpdateTree(None, self.tree)
				self.app.cmp_tree.Bind(wx.EVT_TREE_BEGIN_DRAG, self.BeginDrag)
				trgt = CmpDropTarget(app)
				self.app.dsgn.SetDropTarget(trgt)
				
		def BuildTree(self):
				self.tree = TreeNode("Cmps", True)
				self.tree.isRoot = True
				self.tree.AddNode(TreeNode("Button", False))
				self.tree.AddNode(TreeNode("Canvas", False))
				self.tree.AddNode(TreeNode("CheckBox", False))
				self.tree.AddNode(TreeNode("RadioButton", False))
				self.tree.AddNode(TreeNode("Panel", False))
				self.tree.AddNode(TreeNode("Image", False))
				self.tree.AddNode(TreeNode("List", False))
				self.tree.AddNode(TreeNode("TextArea", False))
				self.tree.AddNode(TreeNode("TextLine", False))
				self.tree.AddNode(TreeNode("TextInput", False))
				self.tree.AddNode(TreeNode("Slider", False))
				self.tree.AddNode(TreeNode("ScrollBar", False))
				self.tree.AddNode(TreeNode("Label", False))
				self.tree.AddNode(TreeNode("ComboBox", False))
				
		def BeginDrag(self, event):
				item = event.GetItem()
				item = self.app.cmp_tree.GetItemText(item)
				dropsrc = wx.DropSource(self.app.frame)
				data = wx.TextDataObject(item)
				dropsrc.SetData(data)
				rst = dropsrc.DoDragDrop(wx.Drag_AllowMove)
						
		def UpdateTree(self, parent, node):
				if node.isRoot:
						root = self.app.cmp_tree.AddRoot(node.name)
						for n in node.children:
								self.UpdateTree(root, n)
						return
				if node.isFolder:
						p = self.app.cmp_tree.AppendItem(parent, node.name)
						for n in node.children:
								self.UpdateTree(p, n)
						return
				self.app.cmp_tree.AppendItem(parent, node.name)
				
				
class LayerMgr():
		def __init__(self, app):
				self.app = app
				
		def BuildTree(self):
				pass
				
		def UpdateTree(self, parent, node):
				if node.isRoot:
						root = self.app.layer_tree.AddRoot(node.name)
						for n in node.children:
								self.UpdateTree(root, n)
						return
				if node.isFolder:
						p = self.app.layer_tree.AppendItem(parent, node.name)
						for n in node.children:
								self.UpdateTree(p, n)
						return
				self.app.layer_tree.AppendItem(parent, node.name)
				
class DsgnMgr():
		def __init__(self, app):
				self.app = app
				self.app.dsgn.Bind(wx.EVT_MOTION, self.Motion)
				
		def Motion(self, event):
				print "mouse move"
				
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
				print "btn left down"
				
		def LeftUp(self, event):
				print "btn left up"