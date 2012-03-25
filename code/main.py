#!/usr/bin/python3


def math(string):
    """ Returns string converted into math mode.
    """
    return '${0}$'.format(string).replace('.', ',')


def currency(string):
    """ Returns in math mode with Lt suffix.
    """
    return math('{0:.2f}Lt'.format(string))


def multiply(value, multiplier):
    return math('{0} \\cdot {1}\% = {2:.2f}Lt'.format(
        value, multiplier, value*multiplier/100))


def half_multiply(value, multiplier):
    return math('{0} \\cdot \\frac{{{1}\%}}{{2}} = {2:.2f}Lt'.format(
        value, multiplier, value*multiplier/200))


class Money:
    """ Abstraction for monetary operations.
    """

    def __init__(self, on_paper):
        self._on_paper = on_paper
        self._to_hands = on_paper
        self._cost = on_paper

    @property
    def on_paper(self):
        return currency(self._on_paper)

    @property
    def to_hands(self):
        return currency(self._to_hands)

    @property
    def cost(self):
        return currency(self._cost)

    def tax_employee(self, percent):
        amount = self._on_paper * percent / 100
        self._to_hands -= amount
        return math('{0} \\cdot {1}\% = {2:.2f}Lt'.format(
            self._on_paper, percent, amount))

    def tax_employee_half(self, percent):
        amount = self._on_paper * percent / 200
        self._to_hands -= amount
        return math('{0} \\cdot \\frac{{{1}\%}}{{2}} = {2:.2f}Lt'.format(
            self._on_paper, percent, amount))

    def tax_employer(self, percent):
        amount = self._on_paper * percent / 100
        self._cost += amount
        return math('{0} \\cdot {1}\% = {2:.2f}Lt'.format(
            self._on_paper, percent, amount))

    def tax_employer_half(self, percent):
        amount = self._on_paper * percent / 200
        self._cost += amount
        return math('{0} \\cdot \\frac{{{1}\%}}{{2}} = {2:.2f}Lt'.format(
            self._on_paper, percent, amount))


class Environment:
    """ Pagalbinė klasė LaTeX aplinkų kūrimui.
    """

    def __init__(self, name, *args):
        self.name = name
        self.content = []
        self.args = args

    def __str__(self):
        return '\\begin{{{0}}}{2}\n{1}\n\\end{{{0}}}'.format(
                self.name, ''.join(self.content),
                ''.join(
                    ('[{0}]' if angle_bracket else '{{{0}}}').format(arg)
                    for arg, angle_bracket in self.args))

    def append(self, frmt, *args, **kwargs):
        """ Appends string to content.
        """
        if args or kwargs:
            self.content.append(frmt.format(*args, **kwargs))
        else:
            self.content.append(frmt)


class EnumerateEnvironment(Environment):
    """ Pagalbinė klasė LaTeX enumerate aplinkų kūrimui.
    """

    def __init__(self):
        super(EnumerateEnvironment, self).__init__('enumerate')

    def append(self, frmt, *args, **kwargs):
        """ Appends string to content.
        """
        super(EnumerateEnvironment, self).append(
                '\n\n\\item ' + frmt, *args, **kwargs)


class TableEnvironment(Environment):
    """ Helper class for creating tables.
    """

    def __init__(self, columns):
        self.width = 15
        proportion = self.width / sum(columns)
        super(TableEnvironment, self).__init__(
                'tabularx',
                ('{0}cm'.format(self.width), False),
                ('|'.join(
                    'p{{{}cm}}'.format(proportion * column)
                    for column in columns
                    ), False))

    def add_row(self, *values):
        """
        """
        self.append('{0} \\\\\n'.format(' & '.join(
            str(value) for value in values)))


def echo(*args):
    """ Prints all arguments.
    """

    for i, arg in enumerate(args):
        print('[{0}]: {1}\n\n'.format(i, arg))


def autorine_be_darbo(*args):
    """ Apskaičiuoja viską autorinei be darbo sutarties.
    """
    table = TableEnvironment((1, 1))

    money = Money(int(args[3]))
    table.add_row('Ant popieriaus:', money.on_paper)
    table.add_row('GPM:', money.tax_employee(15))
    table.add_row('PSDF:', money.tax_employee_half(9))
    table.add_row('Į rankas:', money.to_hands)
    table.add_row('VSDF:', money.tax_employer_half(29.7))
    table.add_row('Darbo vietos kaina:', money.cost)

    print(str(table))


def autorine_su_darbu(*args):
    """ Apskaičiuoja viską autorinei be darbo sutarties.
    """
    table = TableEnvironment((1, 1))

    money = Money(int(args[3]))
    table.add_row('Ant popieriaus:', money.on_paper)
    table.add_row('GPM:', money.tax_employee(15))
    table.add_row('PSDF:', money.tax_employee(9))
    table.add_row('Į rankas:', money.to_hands)
    table.add_row('VSDF:', money.tax_employer(30.98))
    table.add_row('Darbo vietos kaina:', money.cost)

    print(str(table))


if __name__ == '__main__':
    import sys
    locals()[sys.argv[1].replace('|', '_')](*sys.argv)
