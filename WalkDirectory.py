import os
import wx

class WalkDirectory(object):

    def wolkDir(self, treeObj: wx.TreeCtrl, item, path):
        for root, dirs, files in os.walk(path):
            dirItem = treeObj.AppendItem(item, root)
            for filename in files:
                fileItem = treeObj.AppendItem(dirItem, filename, -1, -1, os.path.join(root, filename) )
                
    def wolkDirAppenTree(self, treeObj: wx.TreeCtrl, path):
        treeObj.DeleteAllItems()
        treeRoot = treeObj.AddRoot("Path")
        self.wolkDir(treeObj, treeRoot, path)
        treeObj.Expand(treeRoot)
