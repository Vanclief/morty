class Tcolors:
    def __init__(self):
        self.header = '\033[0;30;47m'
        self.bold = '\033[1;37;40m'
        self.blue = '\033[0;34;40m'
        self.cyan = '\033[0;36;40m'
        self.yellow = '\033[0;33;40m'
        self.green = '\033[0;32;40m'
        self.red = '\033[0;31;40m'
        self.b_green = '\033[0;37;42m'
        self.b_red = '\033[0;37;41m'
        self.b_blue = '\033[0;37;44m'
        self.b_yellow = '\033[0;37;43m'
        self.warning = '\033[1:30:41m'
        self.end = '\033[0m'
        self.under = '\033[4m'

    def colorize_i(self, color, value):
        return color + str('{:.0f}'.format(value)) + self.end

    def colorize_f(self, color, value):
        return color + str('{:.4f}'.format(value)) + self.end

    def colorize_s(self, color, string):
        return color + string + self.end

    def polarize_f(self, value):
        # This is a shitty function name, but Im tired so fuck it well roll with
        # it
        if (value >= 0):
            return self.green + str(' {:.2f}'.format(value)) + self.end

        return self.red + str('{:.2f}'.format(value)) + self.end

    def polarize_s(self, string):
        if (string == 'open '):
            return self.b_green + string + self.end
        elif (string == 'close'):
            return self.b_red + string + self.end
        elif (string == 'long'):
            return self.b_blue + string + " " + self.end

        return self.b_yellow + string + self.end




