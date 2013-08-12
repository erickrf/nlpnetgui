# -*- coding: utf-8 -*-

from itertools import izip
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
        self.label_in = wx.StaticText(self, label='Text to tag:')
        self.text_in = wx.TextCtrl(self,
                                   style=wx.TE_MULTILINE)
        self.output = wx.StaticText(self, label='Output:')
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
        
        self.pos_tagger = run.tag_pos()
        self.srl_tagger = run.tag_srl()
    
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
        tagged_sents = run.tag_text(text, tagger)
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
        
        for sent, tags in tagged_sents:
            zipped = zip(sent, tags)
            tagged_str = ' '.join('_'.join(token) for token in zipped)
            self.text_out.AppendText('%s\n' % tagged_str)
    
    def _display_result_srl(self, tagged_sents):
        '''
        Displays the resulting tagged text in the output area, in a 
        format fit for SRL, where tokens have one label per predicate.
        @param tagged_sents: a tuple in the format (tokens, (predicates, tags))
        The tokens list should be a simple list of strings.
        The predicates list should have one item for each token.
        The tags are a list of lists, one for each predicate,
        containing the tags for the tokens. 
        '''
        self.text_out.Clear()
        for sent in tagged_sents:
            tokens, preds_and_tags = sent
            predicates, tags = preds_and_tags
            max_verb_len = max(len(token) for token in predicates)
            format_str = u'{:<%d}' % (max_verb_len + 1)
            predicates = [format_str.format(pred) for pred in predicates]
            
            # the asterisk tells izip to treat the elements in the list as separate arguments
            the_iter = izip(tokens, predicates, *tags)
            for token_and_tags in the_iter:
                sent_str = '\t'.join(token_and_tags).encode('utf-8')
                self.text_out.AppendText('%s\n' % sent_str)
            
            # line break after each sent
            self.text_out.AppendText('\n')
    
    def set_input_text(self, text):
        '''
        Shows the given text in the input text field.
        '''
        self.text_in.SetValue(text)
    
    