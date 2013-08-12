# -*- coding: utf-8 -*-

'''
Main script for running the NLPNET GUI.
'''

import os
import wx

import main_panel

# the whole system version
VERSION = '1.0'

class MainWindow(wx.Frame):
    '''
    Main interface class for the program.
    '''
    
    def __init__(self, title):
        # show a splash screen while the taggers are loaded
        splash = self._show_splash()
        
        # start the frame occupying 70% of the display.
        # seems a good proportion
        x, y = wx.DisplaySize()
        wx.Frame.__init__(self, parent=None, title=title, 
                          size=(0.7*x, 0.7*y))
        
    
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
        
        splash.Destroy()
        self.Show()
    
    def _show_splash(self):
        '''
        Shows a splash screen. Simple as that.
        '''
        bitmap = wx.Bitmap('../splash.bmp')
        splash = wx.SplashScreen(bitmap, wx.SPLASH_CENTRE_ON_PARENT,
                                 0, None)
        splash.Show()
        return splash
    
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
            self.panel.set_input_text(text)
        
        dialog.Destroy()
        
        
    def on_about(self, event):
        info = wx.AboutDialogInfo()
        info.SetName('NLPNET Graphical User Interface')
        info.SetVersion(VERSION)
        info.SetWebSite('https://github.com/erickrf/nlpnet')
        with open('../desc.txt', 'r') as f:
            text = f.read()
        info.SetDescription(text)
        
        wx.AboutBox(info)
    
    def on_exit(self, event):
        """
        Closes the application.
        """
        self.Close()


app = wx.App(False) 
frame = MainWindow("NLPNET Graphical User Interface")
app.MainLoop()
