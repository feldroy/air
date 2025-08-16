class CSSVariables:
    def __init__(self, ruleset: str|None=':root', **kwargs):
        self.ruleset = ruleset
        for k,v in kwargs.items():
            if isinstance(v, (str, int, float)):
                setattr(self, k, v)
            else:
                raise AttributeError('CSSVariables only accpets str, int, and float for CSS variables')

    def render(self) -> str:
        result = f'{self.ruleset}{{\n'
        for var_name,var_value in self.__dict__.items():
            if var_name=='ruleset': continue
            result += f'  --{var_name.replace('_', '-')}: {var_value};\n'
        result += '}\n\n'
        return result


