from mistune import escape, Markdown, escape_html
from mistune.renderers import BaseRenderer
import re
FORMULA_PATTERN = re.compile(r"\$\$\n((.+\n)*)\$\$")
VAR_PATTERN = r"\{(.+)}"
KAY_PATTERN = r"关键字：((.+)*)"
# FORMULA_PATTERN.match().


def parse_formula(self, m, state):
    text = m.group(1)
    array_pattern = re.compile(r"\\array\{(.*)}")
    array_pattern.sub(text, text)
    return {'type': 'block_formula', 'text': text}


def render_tex_formula(text):
    return '\n\\begin{equation}\n' + text + '\\end{equation}\n'


def parse_key(self, m, state):
    text = m.group(1)
    return 'keywords', text


def render_tex_key(text):
    return r"\keywords{" + text.replace('，', r"\quad ") + "}"


def parse_var(self, m, state):
    text = self.var[m.group(1)]
    return {'type': 'inline_formula', 'text': text}


def render_tex_var(text):
    return '$' + text + '$'


def plugin_pytex(md):
    md.block.register_rule('formula', FORMULA_PATTERN, parse_formula)
    md.block.rules.append('formula')
    md.inline.register_rule('keywords', KAY_PATTERN, parse_key)
    md.inline.rules.append('keywords')
    # md.inline.register_rule('var', VAR_PATTERN, parse_var)
    # md.inline.rules.append('var')

    if md.renderer.NAME == 'tex':
        md.renderer.register('formula', render_tex_formula)
        md.renderer.register('keywords', render_tex_key)
        # md.renderer.register('var', render_tex_var)


class Renderer(BaseRenderer):
    NAME = 'tex'
    IS_TREE = False

    def __init__(self, escape=False, **var):
        super().__init__()
        self._escape = escape
        self.var = var

    def text(self, text):
        return text.replace("%", r"\%")

    def link(self, link, text=None, title=None):
        if text is None:
            text = link
        return f"\\href{{{link}}}{{{text}}}"

    def image(self, src, alt="", title=None): #这里需要改bug 看原始的render是怎么写的
        return f"\\includegraphics[]{{{src}}}"

    def emphasis(self, text):
        return '\\emph{' + text + '}'

    def strong(self, text):
        return '\\textbf{' + text + '}'

    def codespan(self, text):
        # return '<code>' + escape(text) + '</code>'
        return text

    def linebreak(self):
        return '\\newline\n'

    def inline_html(self, html):
        if self._escape:
            return escape(html)
        return html

    def paragraph(self, text):
        return '\n' + text + '\n'

    def heading(self, text, level):
        tag = "sub"*(level-1)+"section"
        return f'\\{tag}{{{text}}}\n'

    def newline(self):
        return ''

    def thematic_break(self):
        # return '<hr />\n'
        return '\n'

    def block_text(self, text):
        return text

    def block_code(self, code, info=None):
        if info is not None:
            info = info.strip()
        if info == 'pseudocode':
            patterns = [
                re.compile(r".*function (.*)\((.*)\)"),
                re.compile(r".*else if (.*)"),
                re.compile(r".*if (.*)"),
            ]
            commands = ['Function', "ElsIf", 'If', ]
            code = code.split("\n")
            out = '\\begin{algorithm}\n'
            out += f'\\caption{{{code[0]}}}\n'
            out += '\\begin{algorithmic}[1]\n'
            out += f'\\Require{{{code[1]}}}\n'
            out += f'\\Ensure{{{code[2]}}}\n'
            stack = []
            for c in code[3:-1]:
                c = c.strip()
                i = -1
                p = None
                for pattern in patterns:
                    i += 1
                    p = pattern.search(c)
                    if p is not None:
                        out += f'\\{commands[i]}'
                        for g in p.groups():
                            out += f"{{{g}}}"
                        out += "\n"
                        stack.append(i)
                        break
                if p is not None:
                    continue
                if c == 'end':
                    mode = stack.pop()
                    while mode == 1:
                        mode = stack.pop()
                    if mode == 0:
                        out += "\\EndFunction\n"
                    elif mode == 2:
                        out += "\\EndIf\n"
                elif c == "else":
                    out += "\\Else\n"
                else:
                    out += r"\State{" + c + "}\n"

            out += '\\end{algorithmic}\n\\end{algorithm}'
            return out
        elif info:
            out = r"\begin{lstlisting}[language = {"
            out += info
            out += "}]\n"
            out += escape(code)
            out += '\\end{lstlisting}\n'
            return out

    def block_quote(self, text):
        return '<blockquote>\n' + text + '</blockquote>\n'

    def block_html(self, html):
        if not self._escape:
            return html + '\n'
        return '\n' + escape(html) + '\n'

    def block_error(self, html):
        return '<div class="error">' + html + '</div>\n'

    def list(self, text, ordered, level, start=None):
        if ordered:
            ordered = "enumerate"
        else:
            ordered = "itemize"
        return f'\\begin{{{ordered}}}\n{text}\\end{{{ordered}}}\n'

    def list_item(self, text, level):
        return '\\item\n' + text + '\n'


markdown = Markdown(Renderer(), plugins=[plugin_pytex])

if __name__ == '__main__':
    markdown = Markdown(Renderer(), plugins=[plugin_pytex])
    print(markdown("``"))
