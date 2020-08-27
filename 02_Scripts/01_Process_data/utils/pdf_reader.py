import fitz
import camelot
import pikepdf
import numpy as np
import re
import pandas as pd


class PdfExtractVariables:
    def __init__(self, file_name):
        # Store filename and decrypted filename
        self.filename = file_name
        self.dec_filename = self.filename.replace('.pdf', '_dec.pdf')

        # Decrypt using pikepdf
        pdf = pikepdf.open(self.filename)
        pdf.save(self.dec_filename)

        # Get fitz file and number of pages
        self.file_fitz = fitz.open(self.dec_filename)
        self.pageCount = self.file_fitz.pageCount

    def get_databases_list(self):
        # Create lists for data names and descriptions
        databases_list = []
        databases_descriptions = []

        # Loop over each page in the document and read
        for page_num in np.arange(0, self.pageCount):
            page = self.file_fitz.loadPage(int(page_num))
            page_text = page.getText('text')

            # Get database if any
            data_name = re.findall(r"Archivo: (.+).dbf", page_text)
            data_description = re.findall(r"dbf \(((?s:.+))\)", page_text)

            # Append to database list and data descriptions list
            if data_name:
                databases_list.append(data_name[0])
                databases_descriptions.append(data_description[0])
            else:
                databases_list.append(None)
                databases_descriptions.append(None)

        return databases_list, databases_descriptions

    def get_page_table(self, page):
        table = camelot.read_pdf(self.dec_filename, pages=str(page),
                                 copy_text='v')

        if table.n == 0:
            table = camelot.read_pdf(self.dec_filename, pages=str(page),
                                     copy_text='v', line_scale=60)
            if table.n == 0:
                print("Could not find a table on page {} of pdf {} using lattice. Will attempt to use column "
                      "coordinates provided.".format(page, self.dec_filename))
                table = camelot.read_pdf(self.dec_filename, pages=str(page),
                                         flavor='stream',
                                         columns=['58.55,113.75,172.07,362.64,412.08,456.0,661.12'],
                                         row_tol=1000, column_tol=1000)
                if table.n == 0:
                    raise Exception("Could not find a table on page {} of pdf {}.".format(page, self.dec_filename))
        return table[0].df

    def get_databases(self, databases_list, databases_descriptions):
        # Create database dictionary
        databases = {}

        # Create holding variable for current table
        current_table = ''

        # Loop over each page in the pdf
        for (page, (data_name, data_desc)) in enumerate(zip(databases_list, databases_descriptions)):
            # Get table for current page (we add 1 as Camelot is not zero-based)
            table = self.get_page_table(page=page + 1)

            if data_name is not None:
                databases[data_name] = [data_desc, table]
                current_table = data_name
            else:
                databases[current_table][1] = pd.concat([databases[current_table][1], table])

        return databases
