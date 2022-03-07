import zipfile
import xml.etree.ElementTree as ET

def traverse_xml(root):
    if root == None:
        print("Element is None")
        return

    for element in root:
        print(element.tag, element.attrib)
        traverse_xml(element)

def read_pptx_xml():
    with zipfile.ZipFile("./result/xml/table.pptx.zip") as table_pptx_zip:
        with table_pptx_zip.open("ppt/slides/slide1.xml") as slide1_xml:
            content = slide1_xml.read()
            #src_xml = ET.parse(slide1_xml)

    #print(src_xml.text)
    with zipfile.ZipFile('./result/xml/test.pptx.zip', 'w') as archive:
        with archive.open('ppt/slides/slide1.xml') as slide1_xml:
            #slide1_xml.write(content)
            pass

    #print(text)
    # root = xml_file.getroot()
    # traverse_xml(root)




if __name__ == "__main__":
    read_pptx_xml()
