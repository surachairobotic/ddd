import convertapi

class Convert:
    def DOCXtoPDF(self, docx, pdf):
        convertapi.api_secret = 'oL7HYyv8aMGTQEtX'
        result = convertapi.convert('pdf', { 'File': docx })

        # save to file
        result.file.save(pdf)
