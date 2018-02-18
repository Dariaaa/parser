from codecs import open as open

class Writer:
    @staticmethod
    def write(filename,text):
        with open(filename, "w") as text_file:
            text_file.write(text)
    @staticmethod
    def write_xml(xml_path,xml):
        file = open(xml_path, 'w', encoding='utf8')
        xml.writexml(file, indent="  ", addindent="  ", newl='\n')
        file.close()
