import os

class Postscript:
    """
         2013-08-30:
             Wrapper for creating postscript documents. 
             Right now it's very simple. Later it'll use subprocess like it ought.
    """

    NORMAL_FONT = "Palatino-Roman10"
    HEADER_FONT = "Palatino-Bold10"
    CODE_FONT = "Courier-New10"
    

    def __init__(self, net_id, module_name, output_home="./output"):
        if not os.path.exists(output_home):
            os.mkdir(output_home)
        module_dir = "%s/%s" % (output_home, module_name)
        if not os.path.exists(module_dir):
            os.mkdir(module_dir)
        enscript_command = " ".join([
            'enscript',
            '--quiet',
            '-p',
            "%s/%s-%s.ps" % (module_dir, net_id, module_name),
            '-b', 
            "'%s\t\t%s.ml'" % (net_id, module_name),
            '-M',
            'Letter',
            '--fancy-header',
            '--quiet',
            '--escapes=\001',
            '--no-formfeed',
        ])
        # self.enscript_process = subprocess.Popen(enscript_command, shell=True)
        # self.enscript_process = os.popen(enscript_command)
        # return self.enscript_process.stdin
        self.enscript_stream = os.popen(enscript_command, 'w')

    def change_font(self, font):
        self.enscript_stream.write("\n\001font{%s}" % font)

    def close(self):
        self.enscript_stream.close()

    def write(self, message):
        self.enscript_stream.write(message)

    def write_code(self, filename):
        """
            2013-08-30:
                Write the code to the postscript file,
        """
        self.change_font(self.CODE_FONT)
        with open(filename, 'r') as f:
            for line in f:
                self.enscript_stream.write(line)

    def write_failures(self, failures):
        self.change_font(self.HEADER_FONT)
        self.enscript_stream.write("\nTest failures:\n")
        self.change_font(self.NORMAL_FONT)
        for fail_tuple in failures:
            self.enscript_stream.write("%s : %s\n" % fail_tuple)
        
    def write_nocompile(self, message):
        self.change_font(self.HEADER_FONT)
        self.enscript_stream.write("\nNO COMPILE:\n")
        self.change_font(self.CODE_FONT)
        self.enscript_stream.write("%s" % message)

    def write_success(self):
        self.change_font(self.HEADER_FONT)
        self.enscript_stream.write("\nALL TESTS PASS!\n")
