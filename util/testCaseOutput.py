import re

from util.stackOverflowException import StackOverflowException

class TestCaseOutput:
    """
        2013-09-08:
            Take the string output by an OCaml toplevel
            parse it for warnings, errors, stack overflows, and the like.
    """

    def __init__(self, output, error, debug=False):
        if debug:
            print(output)
            print(error)
        self.output = output
        self.error = error
        self._check_stackoverflow()
        self.errors = self._errors()
        self.warnings = self._warnings()
        self.debug = self._debug()

    def serialize(self):
        """
            2013-09-08:
                Print all warnings and exceptions
        """
        out = []
        if self.warnings:
            out.append(self.warnings)
        if self.errors:
            out.append(self.errors)
        return "\n***\n".join(out)

    def _check_stackoverflow(self):
        if "Stack overflow during evaluation" in self.output:
            raise StackOverflowException

    def _debug(self):
        """
            2013-09-08:
                Debug output is everything that's not a warning or error. 
                For now, just ignore it.
        """
        pass
        
    def _errors(self):

        return (self.error or self._parse_errors()).strip()

    def _parse_errors(self):
        """
            2013-09-08:
                Regex search for exceptions raised during toplevel
        """
        match = re.search(r"#.*?(Exception:[\s].*)\n#", self.output, re.DOTALL)
        if match is not None:
            return match.group(1)
        else:
            return ""

    def _warnings(self):
        match = re.search(r"#.*?(Warning:[\s].*)\n#", self.output, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            return ""
