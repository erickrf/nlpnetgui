# -*- coding: utf-8 -*-

import os
import wx

import nlpnet

class MainPanel(wx.Panel):
    '''
    The main panel for the NLPNET application.
    There is a text area where text can be written or loaded,
    and another for displaying results.
    '''
    
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self._init_grid()
        
        self.Bind(wx.EVT_BUTTON, self.on_run, self.button_run)
        self.Bind(wx.EVT_BUTTON, self.on_load, self.button_load)
        self.Bind(wx.EVT_BUTTON, self.on_save, self.button_save)
        
        nlpnet.set_data_dir('data')
        self.pos_tagger = nlpnet.POSTagger()
        self.srl_tagger = nlpnet.SRLTagger()
    
    def _init_grid(self):
        '''
        Initializes the grid containing the panel's objects.
        A flexible grid main_sizer is used to allow a top row with 
        labels, a second with buttons, then a third row with the text
        areas.
        '''
        # the two text areas
        # one for the input text and the other for the output
        label_in = wx.StaticText(self, label='Text to tag')
        self.button_load = wx.Button(self, label='Load')
        self.text_in = wx.TextCtrl(self,
                                   style=wx.TE_MULTILINE)
        label_out = wx.StaticText(self, label='Output')
        self.button_save = wx.Button(self, label='Save')
        self.text_out = wx.TextCtrl(self,
                                   style=wx.TE_MULTILINE)
        
        self.button_run = wx.Button(self, label="Run")
        self.radio_pos = wx.RadioButton(self, label='POS', style=wx.RB_GROUP)
        self.radio_srl = wx.RadioButton(self, label='SRL')
        
        button_box = wx.StaticBox(self, label="Options")
        button_sizer = wx.StaticBoxSizer(button_box, wx.VERTICAL)
        button_sizer.Add(self.button_run, 1, 
                              flag=wx.ALIGN_CENTER | wx.EXPAND | wx.ALL,
                              border=5)
        button_sizer.Add(self.radio_pos, 1)
        button_sizer.Add(self.radio_srl, 1)
        
        main_sizer = wx.FlexGridSizer(rows=3, cols=3, vgap=10, hgap=5)
        
        # top row, only labels
        main_sizer.Add(label_in)
        main_sizer.Add((0, 0)) # empty cell
        main_sizer.Add(label_out)
        
        # middle row, buttons
        main_sizer.Add(self.button_load)
        main_sizer.Add((0, 0)) # empty cell
        main_sizer.Add(self.button_save)
        
        # bottom row, text areas and the main command
        main_sizer.Add(self.text_in, 1, wx.EXPAND)
        main_sizer.Add(button_sizer)
        main_sizer.Add(self.text_out, 1, wx.EXPAND)
        
        # the second row contains the text areas in the first and 
        # third columns
        main_sizer.AddGrowableRow(2, 1)
        main_sizer.AddGrowableCol(0, 1)
        main_sizer.AddGrowableCol(2, 1)
        
        # add an outer box main_sizer to insert borders
        outer_sizer = wx.BoxSizer(wx.HORIZONTAL)
        outer_sizer.Add(main_sizer, 1, wx.ALL | wx.EXPAND, border=10)
        
        self.SetSizer(outer_sizer)
    
    def on_load(self, event):
        '''
        Opens a file to be processed.
        '''
        dialog = wx.FileDialog(self, "Choose a text file", style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetFilename()
            dirname = dialog.GetDirectory()
            path = os.path.join(dirname, filename)
            
            try:
                with open(path, 'r') as f:
                    text = f.read()
                print type(text)
                utext = text.decode('utf-8')
            except UnicodeDecodeError:
                dlg = wx.MessageDialog(self, 'Error trying to open file.\n\
Be sure that your input file is encoded in UTF-8 or pure ASCII.',
                                             'Error', style=wx.OK | wx.ICON_ERROR)
                dlg.ShowModal()
                dlg.Destroy()
                return
                
            self.text_in.SetValue(utext)
        
        dialog.Destroy()
    
    def on_save(self, event):
        '''
        Saves the output to a file
        '''
        dialog = wx.FileDialog(self, 'Choose file to save', 
                               style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        dialog.SetFilename('nlpnet-output.txt')
        if dialog.ShowModal() == wx.ID_OK:
            filename = dialog.GetFilename()
            dirname = dialog.GetDirectory()
            path = os.path.join(dirname, filename)
            text = self.text_out.GetValue()
            try:
                with open(path, 'w') as f:
                    f.write(text.encode('utf-8'))
            except IOError:
                error_dlg = wx.MessageDialog(self, 'Error trying to write file.',
                                             'Error', style=wx.OK | wx.ICON_ERROR)
                error_dlg.ShowModal()
                error_dlg.Destroy()
        
        dialog.Destroy()
    
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
        # try to use a cached tagger
        task = task.lower()
        try:
            tagger = getattr(self, '%s_tagger' % task)
        except:
            raise AttributeError('Unknown task: %s' % task)
        
        text = self.text_in.GetValue()
        tagged_sents = tagger.tag(text)
        if task == 'srl':
            self._display_result_srl(tagged_sents)
        else:
            self._display_result_simple(tagged_sents)
        
        
    def _display_result_simple(self, tagged_sents):
        '''
        Displays the resulting tagged text in the output area.
        The simple result means that there is one tag per word, like
        in POS, but not for SRL.
        '''
        self.text_out.Clear()
        
        for sent in tagged_sents:
            tagged_str = ' '.join('_'.join(token) for token in sent)
            self.text_out.AppendText('%s\n' % tagged_str)
    
    def _display_result_srl(self, tagged_sents):
        '''
        Displays the resulting tagged text in the output area, in a 
        format fit for SRL, where tokens have one label per predicate.
        
        :type tagged_sents: nlpnet.taggers.SRLAnnotatedSentence  
        '''
        self.text_out.Clear()
        for sent in tagged_sents:
            
            # print the whole sentence first and then each arg structure
            sentence_str = ' '.join(sent.tokens)
            self.text_out.AppendText('%s\n' % sentence_str)
            
            for arg_struct in sent.arg_structures:
                verb, args = arg_struct
                
                # print the verb in the first line and then the arguments
                self.text_out.AppendText('  %s\n' % verb)
                
                for arg in args:
                    arg_content = ' ' .join(args[arg])
                    self.text_out.AppendText('    %s: %s\n' % (arg, arg_content))
                
                # line break after each arg structure
                self.text_out.AppendText('\n')
            
            # line break after each sent
            self.text_out.AppendText('\n')
    
    
    