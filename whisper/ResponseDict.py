import os
import itertools
class ResponseDict:
    '''セリフ集です'''
    @property
    def WhoAreYou(self):
        return tuple(itertools.product(
            ("君", "きみ", "あなた", "貴方"), 
            ("は",),
            ("誰", "だれ"),
            ("", "？", "?")))

    @property
    def IamWhisper(self):
        return "私はwhisperです。" + os.linesep + "どなたとお話ししますか?"

    @property
    def IamPlant(self):
        return tuple(itertools.product(
            ("私は", ), ("%s", ) ,("です。", "だよ。"), 
            (os.linesep + "よろしくね!", "")
        ))
    
    @property
    def NobodySpeaking(self):
        return "誰ともお話ししてないよ"

    

Instance = ResponseDict()