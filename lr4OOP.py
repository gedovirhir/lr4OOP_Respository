import clr
import random
import time
from abc import ABC, abstractmethod

clr.AddReference('System')
clr.AddReference('System.IO')
clr.AddReference('System.Drawing')
clr.AddReference('System.Reflection')
clr.AddReference('System.Threading')
clr.AddReference('System.Windows.Forms')

import System.IO
import System.Drawing as Dr
import System.Reflection
import System.Windows.Forms as WinForm

class __storageList__(ABC): #снаружи наше "хранилище" ведет себя как список
    @abstractmethod
    def __init__(self): #ининциализация списка
        pass
    def add(self, x, index): #добавление элемента по индексу
        pass
    def getNode(self, index): #получение узла по индексу
        pass
    def cotnains(self, name): #проверка наличия элемента в узлах списка
        pass
    def isEmpty(self): #проверяет список на наличие хотя бы 1го элемента 
        pass
    def deleteIndex(self, index): #удаление элемента по индексу
        pass
    def clear(self): #очистка списка
        pass 

class Node(object):
    def __init__(self, x = None, v = None):
        self.key = x
        self.next = None
        self.prev = v

class CCircleStorage(__storageList__):
    def __init__(self):
        self.head = None
        self.len = 0
    
    def add(self, x, index = None):
        newNode = Node(x)
        if self.head is None:
            self.head = newNode
            self.len += 1
            return
        lastNode = self.head
        if index:
            for i in range(index):
                if (lastNode.next):
                    lastNode = lastNode.next
        else:
            while lastNode.next:
                lastNode = lastNode.next
        if lastNode.next:
            lastNode.next.prev = newNode
            newNode.next = lastNode.next
        lastNode.next = newNode
        newNode.prev = lastNode
        self.len += 1
    
    def getNode(self, index):
        if index > self.len-1: IndexError("IndexError")
        lastNode = self.head
        for i in range(index):
            lastNode = lastNode.next
        return lastNode
    
    def cotnains(self, name):
        lastNode = self.head
        while (lastNode):
            if name == lastNode.key:
                return True
            else:
                lastNode = lastNode.next
        return False

    def isEmpty(self):
        if self.head:
            return False
        else:
            return True

    def deleteIndex(self, index):
        lastNode = self.head
        if index == 0:
            self.head = lastNode.next
            if lastNode.next:
                lastNode.next.prev = None
            self.len -= 1
            return
        lastNode = self.getNode(index)
        
        if lastNode.next is not None:
            lastNode.next.prev = lastNode.prev
        lastNode.prev.next = lastNode.next

        del lastNode
        self.len -= 1

    def clear(self):
        for i in range(self.len):
            self.deleteIndex(0)

    def exclusiveSelect(self, node):
        forwardNode = node.next
        prevNode = node.prev
        node.key.selected = True
        while forwardNode:
            forwardNode.key.selected = False
            forwardNode = forwardNode.next
        while prevNode:
            prevNode.key.selected = False
            prevNode = prevNode.prev
    def inclusiveSelect(self, node):
        node.key.selected = True

    

class CCircle(object):
    def __init__(self, x, y):
        self.xcord = x
        self.ycord = y
        self.rad = 15

        self.selected = False


class form1(System.Windows.Forms.Form):
    def __init__(self):        
        self.Text = "form"
        self.BackColor = Dr.Color.FromArgb(238,238,238)
        self.ClientSize = Dr.Size(900,900)
        caption_height = WinForm.SystemInformation.CaptionHeight
        self.MinimumSize =Dr.Size(392,(117 + caption_height))
        self.KeyPreview  = True
        self.CtrlPressed = False

        self.canvas = Dr.Bitmap(700,700)
        self.CircleStorage = CCircleStorage()
        self.drawPen = Dr.Pen(Dr.Brushes.DeepSkyBlue)
        self.drawPen.Width = 2
        self.flagGraphics = Dr.Graphics.FromImage(self.canvas)

        self.drawPen2 = Dr.Pen(Dr.Brushes.Purple)
        self.drawPen2.Width = 15
        
        self.InitiliazeComponent()
        
    
    def run(self):
        WinForm.Application.Run(self)
    
    def InitiliazeComponent(self):
        self.components = System.ComponentModel.Container()
        self.ImagePB = WinForm.PictureBox()
        self.butt = WinForm.Button()
        self.KeyDown += self.Form_KeyDown
        self.KeyUp += self.Form_KeyUp

        self.ImagePB.Location = Dr.Point(10, 10)
        self.ImagePB.Size = Dr.Size(700, 700)
        self.ImagePB.TabStop = False
        self.ImagePB.BorderStyle = WinForm.BorderStyle.Fixed3D
        self.ImagePB.MouseDown += self.ImagePB_KeyDown

        self.butt.Location = Dr.Point(10, 720)
        self.butt.Size = Dr.Size(200, 50)
        self.butt.BackColor = Dr.Color.FromArgb(238,238,240)
        self.butt.Text = "Очистить"
        self.butt.UseVisualStyleBackColor = 0
        self.butt.FlatStyle = WinForm.FlatStyle.Flat
        self.butt.FlatAppearance.BorderSize = 0
        self.butt.Click += self.butt_Click     
        
        
        self.Controls.Add(self.ImagePB)
        self.Controls.Add(self.butt)
    def dispose(self):
        self.components.Dispose()
        WinForm.Form.Dispose(self)

    def drawAllCircles(self):
        self.ImagePB.Image = None
        self.canvas = Dr.Bitmap(700,700)
        self.flagGraphics = Dr.Graphics.FromImage(self.canvas)
        for i in range(self.CircleStorage.len):
            cr = (self.CircleStorage.getNode(i)).key
            if cr.selected:
                self.flagGraphics.FillEllipse(Dr.Brushes.LightGreen, cr.xcord - cr.rad, cr.ycord-cr.rad, cr.rad*2,cr.rad*2)
                self.flagGraphics.DrawEllipse(self.drawPen,cr.xcord - cr.rad, cr.ycord-cr.rad, cr.rad*2,cr.rad*2)
            else:
                self.flagGraphics.DrawEllipse(self.drawPen,cr.xcord - cr.rad, cr.ycord-cr.rad, cr.rad*2,cr.rad*2)
        self.ImagePB.Image = self.canvas

    def Form_KeyDown(self, sender, args):
        if args.KeyCode == WinForm.Keys.ControlKey:
            self.CtrlPressed = True
    def Form_KeyUp(self, sender, args):
        if args.KeyCode == WinForm.Keys.ControlKey:
            self.CtrlPressed = False


    def ImagePB_KeyDown(self, sender, args):
        if args.Button == WinForm.MouseButtons.Right:
            casualCircle = CCircle(args.X, args.Y)
            self.CircleStorage.add(casualCircle)

            self.drawAllCircles()
        elif args.Button == WinForm.MouseButtons.Left:
            for i in range(self.CircleStorage.len):
                casualNode = self.CircleStorage.getNode(i)
                casualCirc = casualNode.key
                if ((casualCirc.xcord + casualCirc.rad)>args.X>(casualCirc.xcord - casualCirc.rad)) and ((casualCirc.ycord + casualCirc.rad)>args.Y>(casualCirc.ycord - casualCirc.rad)):
                    if self.CtrlPressed:
                        self.CircleStorage.inclusiveSelect(casualNode)
                    else:
                        self.CircleStorage.exclusiveSelect(casualNode)
                    
                    self.drawAllCircles()



                    

        
    def butt_Click(self, sender, args):
        self.ImagePB.Image = None
        self.flagGraphics = Dr.Graphics.FromImage(self.canvas)
        self.CircleStorage.clear()
        self.canvas = Dr.Bitmap(700,700)




def form_thr():
    form = form1()

    WinForm.Application.Run(form)
    form.dispose()


if __name__ == '__main__':
    form_thr()
