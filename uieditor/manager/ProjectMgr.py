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
				
