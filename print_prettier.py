
class printprettier():
    def __init__(self, color, text, indent=0):
        self.text = text
        self.color = color
        self.indent = indent
        if self.text.split(']')[-1].strip() == '?bar':
            self.bar()
        else:
            self.print_prettier()

    def bar(self):
        print('\033[{}m{}\033[0m'.format(self.color, '-' * 50))

    def print_prettier(self):
        print('\033[{}m{}{}\033[0m'.format(self.color, ' ' * self.indent, self.text))



class printred(printprettier):
    def __init__(self, text='?bar'):
        super().__init__(31, f'[BAD] {text}')
    
class printgreen(printprettier):
    def __init__(self, text='?bar'):
        super().__init__(32, f'[GOOD] {text}')

class printyellow(printprettier):
    def __init__(self, text='?bar'):
        super().__init__(33, f'[WARN] {text}')

class printblue(printprettier):
    def __init__(self, text='?bar'):
        super().__init__(34, f'[ID] {text}')
    
class printfinish(printprettier):
    def __init__(self, text='?bar'):
        super().__init__(42, f'[FINAL RESULT]\n\t{text}')

class printcyan(printprettier):
    def __init__(self, text='?bar'):
        super().__init__(36, f'[ID] {text}')
