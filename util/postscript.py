import os, subprocess

class Postscript:
    """
         2013-08-30:
             Simple wrapper for writing postscript documents. 
             Nothing too special, mostly send over the arguments directly and this file
             takes care of the fonts and the particulars of writing the doc.
    """

    NORMAL_FONT = "Palatino-Roman10"
    HEADER_FONT = "Palatino-Bold10"
    CODE_FONT = "Courier-New10"

    def __init__(self, net_id, module_name, output_home="./output"):
        self.module_name = module_name
        self.net_id = net_id
        self.output_home = output_home
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
        self.enscript_stream = subprocess.Popen(enscript_command, shell=True, stdin=subprocess.PIPE).stdin

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

    def write_email(self, subject, message):
        """
            2013-09-01:
                Write an email message to `netid`@cornell.edu
                Store in 'output/email'
        """
        email_dir = "%s/email" % self.output_home
        if not os.path.exists(email_dir):
            os.mkdir(email_dir)
        with open("%s/%s-%s.txt" % (email_dir, self.net_id, self.module_name), 'w') as email_message:
            print>>email_message, message
        with open("%s/%s-%s.sh" % (email_dir, self.net_id, self.module_name), 'w') as f:
            print>>f,(" ".join([
                "mail",
                "-s",
                "'%s'" % subject,
                "'%s@cornell.edu'" % self.net_id,
            ]))

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
        # Write an email message
        email_subject = "[CS3110 test harness] compile error"
        email_message = "\n".join([
            "Uh oh! Your submission '%s.ml' did not compile. Compiler output:\n" % self.module_name,
            "\n".join(message.split("\n")),
            "\n If this was a trivial error, you have until 11:59PM on Saturday to submit a corrected file to CMS. The course staff will diff your new and old submissions invoke a penalty at their discretion.",
            "\n---",
            "Automatically generated message from the CS3110 test harness",
        ])
        self.write_email(email_subject, email_message)

    def write_success(self):
        self.change_font(self.HEADER_FONT)
        self.enscript_stream.write("\nALL TESTS PASS!\n")
