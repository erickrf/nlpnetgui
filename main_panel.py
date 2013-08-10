# -*- coding: utf-8 -*-

import wx

import run

class MainPanel(wx.Panel):
    '''
    The main panel for the NLPNET application.
    There is a text area where text can be written or loaded,
    and another for displaying results.
    '''
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        
        # the two text areas
        # one for the input text and the other for the output
        self.text_in = wx.TextCtrl(self,
                                   style=wx.TE_MULTILINE)
        self.text_out = wx.TextCtrl(self,
                                   style=wx.TE_MULTILINE)
        
        button = wx.Button(self, label="Run")
        self.Bind(wx.EVT_BUTTON, self.on_run, button)
        self.radio_pos = wx.RadioButton(self, label='POS', style=wx.RB_GROUP)
        self.radio_srl = wx.RadioButton(self, label='SRL')
        
        sb_buttons = wx.StaticBox(self, label="Options")
        self.button_sizer = wx.StaticBoxSizer(sb_buttons, wx.VERTICAL)
        self.button_sizer.Add(button, 1, 
                              flag=wx.ALIGN_CENTER | wx.EXPAND | wx.ALL,
                              border=5)
        self.button_sizer.Add(self.radio_pos, 1)
        self.button_sizer.Add(self.radio_srl, 1)
        
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.text_in, 1, wx.ALL | wx.EXPAND, border=10)
        self.sizer.Add(self.button_sizer)
        self.sizer.Add(self.text_out, 1, wx.ALL | wx.EXPAND, border=10)
        
        self.SetSizer(self.sizer)
        
        # cached models for efficiency
        self.pos_tagger = None
        self.srl_tagger = None
    
    def on_run(self, event):
        '''
        Handler to be called when the run command is issued.
        '''
        if self.text_in.GetValue() == '':
            dialog = wx.MessageDialog(self,
                                      'Load text to be tagged!', style=wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            return
        
        task = None
        if self.radio_pos.GetValue():
            task = 'pos'
        elif self.radio_srl.GetValue():
            task = 'srl'
        else:
            dialog = wx.MessageDialog(self, 'Choose a task.', style=wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
        
        if task is not None:
            self.tag_text(task)
    
    def tag_text(self, task):
        '''
        Tags the input task according to the given task. The text
        must have already been loaded.
        @param task: either 'pos' or 'srl'
        '''
        if task.lower() == 'pos':
            # try to load cached tagger
            if self.pos_tagger is None:
                tagger = run.tag_pos(False, False)
                self.pos_tagger = tagger
            else:
                tagger = self.pos_tagger
                
        elif task.lower() == 'srl':
            dialog = wx.MessageDialog(self, 'SRL not implemented :(', 'Oops...',
                                      wx.OK)
            dialog.ShowModal()
            dialog.Destroy()
            return
        else:
            raise AttributeError('Unknown task: %s' % task)
        
        self.text_out.Clear()
        text = self.text_in.GetValue()
        tagged_sents = run.tag_text(text, tagger)
        for sent, tags in tagged_sents:
            zipped = zip(sent, tags)
            tagged_str = ' '.join('_'.join(token) for token in zipped)
            self.text_out.AppendText('%s\n' % tagged_str)
        
        
    
    def set_input_text(self, text):
        '''
        Shows the given text in the input text field.
        '''
        self.text_in.SetValue(text)
    
    