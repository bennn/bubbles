import subprocess

class SubprocessWrapper:
    """
        2013-09-07:
            Wrapper for executing and cleaning up python subprocess calls.
            
    """

    def execute(self, command, on_failure=None):
        """
            2013-09-07:
                Commonalities are..
                - shell=True
                - run one simple command

                Nocompiles use stderr

                Optional argument `on_failure` is a continuation for failures.
                If the subprocess call fails, it will execute the supplied function
                with the raised exception as its argument. 
                Default is to raise the exception
        """
        output = None
        # Try to run the command, watch for failures
        # Need to close pipe in a finally block? I think not but leaving note just.in.case
        try:
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as cpe:
            if on_failure is None:
                raise cpe
            else:
                return on_failure(cpe)
        # Success! Convert the output to string
        if not isinstance(output, str):
            # 2013-09-07: Explicitly convert bytestring to str, for python 3
            output = output.decode('utf-8')
        return output
