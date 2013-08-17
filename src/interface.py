# -*- coding: utf-8 -*-

'''
Main script for running the NLPNET GUI.
'''

import wx

import main_panel
import guiconfig

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
        
        # task bar icon
        ico = wx.Icon(guiconfig.ICON, wx.BITMAP_TYPE_ICO)
        self.SetIcon(ico)
        
        self.CreateStatusBar()
        
        menu_program = wx.Menu()
        item_about = menu_program.Append(wx.ID_ABOUT, "&About", 
                                         "Information about this program")
        menu_program.AppendSeparator()
        item_exit = menu_program.Append(wx.ID_EXIT,"E&xit", 
                                        "Terminate the program")
        
        self.Bind(wx.EVT_MENU, self.on_about, item_about)
        self.Bind(wx.EVT_MENU, self.on_exit, item_exit)
        
        menubar = wx.MenuBar()
        menubar.Append(menu_program, "&Program")
        self.SetMenuBar(menubar)
        
        self.panel = main_panel.MainPanel(self)
        
        splash.Destroy()
        self.Show()
    
    def _show_splash(self):
        '''
        Shows a splash screen. Simple as that.
        '''
        bitmap = wx.Bitmap(guiconfig.SPLASH)
        splash = wx.SplashScreen(bitmap, wx.SPLASH_CENTRE_ON_PARENT,
                                 0, None)
        splash.Show()
        return splash
    
    def on_about(self, event):
        info = wx.AboutDialogInfo()
        info.SetName('NLPNET Graphical User Interface')
        info.SetVersion(VERSION)
        info.SetWebSite('https://github.com/erickrf/nlpnet')
        with open(guiconfig.DESCRIPTION, 'r') as f:
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
