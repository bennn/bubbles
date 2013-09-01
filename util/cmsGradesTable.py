import cgi, os

class CmsGradesTable:
    """
        2013-09-01:
            Abstraction for posting test harness output to CMS
    """

    def __init__(self):
        """
            2013-09-01:
                Create the grades table.
                For now, store it in memory as a list and only export to 
                a file when prompted. 

                Later, this should probably take a file name as the first argument
        """
        self.table = [
            ["NetID","Grade","Add Comments"],
        ]

    def add_comment(self, net_id, comment):
        self.table.append([net_id, "", comment])

    def export(self):
        """
            2013-09-01:
                Create a .csv file ready to upload to CMS
        """
        if not os.path.exists("./output"):
            os.mkdir("./output")
        with open("./output/grading_comments.csv", 'w') as f:
            for row in self.table:
                print>>f, ",".join(row)

    def serialize(self, message):
        """
            2013-09-01:
                Convert `message` into a string safe for CMS

                TODO right now:
                - removes " characters (so they don't end the open/closing quotes in the .csv file)
                - htmlserializes: < --- &lt;  and stuff like that
        """
        return cgi.escape("".join(( c for c in message if c != "\"" )))

    def update(self, net_id, errors):
        """
            2013-09-01:
                TODO rename this

                Write the grades table entry for student `net_id` given the test harness
                output `errors`.
        """
        if not errors:
            self.add_comment(net_id, "ALL TESTS PASS")
        else:
            cms_message = ["\"", self._heading(net_id), "<p>"]
            for module_name, errors in errors.iteritems():
                cms_message.append("<hr/>")
                cms_message.append("<h4>%s</h4>" % module_name)
                cms_message.append("<ul>")
                for (test_name, test_message) in errors:
                    serialized = self.serialize(test_message)
                    cms_message.append("<li><b>%s</b> : %s</li>" % (test_name, serialized))
                cms_message.append("</ul>")    
            # Close the paragraph and string
            cms_message.append("</p>\"")
            self.add_comment(net_id, "\n".join(cms_message))

    def _heading(self, net_id):
        return "<h2>Automated test results for %s</h2>" % net_id
