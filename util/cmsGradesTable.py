
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

    def add_comment(self, netId, comment):
        self.table.append([netId, "", comment])

    def export(self, filename):
        """
            2013-09-01:
                Create a .csv file ready to upload to CMS
        """
        if not filename.endswith(".csv"):
            filename += ".csv"
        with open(filename, 'w') as f:
            for row in self.table:
                print>>f, ",".join(row)
