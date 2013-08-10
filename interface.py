# -*- coding: utf-8 -*-

import os
import wx

import main_panel

class MainWindow(wx.Frame):
    '''
    Main interface class for the program.
    '''
    
    def __init__(self, title):
        wx.Frame.__init__(self, parent=None, title=title)
    
        self.CreateStatusBar()
        
        menu_file = wx.Menu()
        item_open = menu_file.Append(wx.ID_OPEN, "&Open file", "Open a file")
        menu_file.AppendSeparator()
        item_about = menu_file.Append(wx.ID_ABOUT, "&About", 
                                     "Information about this program")
        menu_file.AppendSeparator()
        item_exit = menu_file.Append(wx.ID_EXIT,"E&xit", 
                                    "Terminate the program")
        
        self.Bind(wx.EVT_MENU, self.on_open, item_open)
        self.Bind(wx.EVT_MENU, self.on_about, item_about)
        self.Bind(wx.EVT_MENU, self.on_exit, item_exit)
        
        menubar = wx.MenuBar()
        menubar.Append(menu_file, "&File")
        self.SetMenuBar(menubar)
        
        self.panel = main_panel.MainPanel(self)
        
        self.Show()
    
    def on_open(self, event):
        '''
        Opens a file to be processed.
        '''
        dialog = wx.FileDialog(self, "Choose a text file", style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetFilename()
            dirname = dialog.GetDirectory()
            path = os.path.join(dirname, filename)
            with open(path, 'r') as f:
                text = f.read()
        dialog.Destroy()
        self.panel.set_input_text(text)
        
    def on_about(self, event):
        dialog = wx.MessageDialog(self, "This is a graphical interface for using the \
NLPNET tool. Developed by Erick Rocha Fonseca (erickrfonseca@gmail.com).", 
            "NLPNET Graphical User Interface", wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
    
    def on_exit(self, event):
        """
        Closes the application.
        """
        self.Close()


app = wx.App(False) 
frame = MainWindow("NLPNET Graphical User Interface")
app.MainLoop()
