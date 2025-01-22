import os
import json
from lxml import html

def extract_elements_from_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    #Cleaning the content just in case there are errors we are not interested
    content = content.splitlines()
    if content[0].startswith('<?xml'):
        content = content[1:]  # Delete the XML declaration line

    tree = html.fromstring('\n'.join(content))  

    #Extract all the tables
    tables = tree.xpath("//*[@class='ltx_table']")
    extracted_data = {}
    
    for idx, table in enumerate(tables):
        table_id = f"id_table_{idx + 1}"
        table_id2 = table.get("id")
        
        #Xpath for captions
        caption = tree.xpath(f"(//*[@class='ltx_table'])[{idx + 1}]//*[contains(@class, 'ltx_caption')]//text()")
        caption_text = ''.join(text for text in caption)
        

        #Table passed from html to string
        html_table = html.tostring(table, encoding='unicode')
        
        
        #Xpath for the foodnotes
        footnotes_hrefs = tree.xpath(f"(//*[@class='ltx_table'])[{idx + 1}]////tbody//a[@class='ltx_ref']/@href")
        list_footnotes = []
        for href in footnotes_hrefs:
            footnote_id = href.lstrip("#")
            footnote_content = tree.xpath(f"//*[@id[contains(., '{footnote_id}')]]")
            if footnote_content:
                list_footnotes.append(footnote_content[0].text_content().strip())


        #Xpath for the referencies
        href_xpath = f"//a[contains(@href, '{table_id2}')]/ancestor::p"
        referencias = tree.xpath(f"{href_xpath}//text()")
        referencias_texto = ''.join(referencias).strip()

        extracted_data[table_id] = {
            'caption': caption_text,
            'table': html_table,
            'footnotes': list(set(list_footnotes)), #dont wanna have repeated values, just in case
            'references': referencias_texto
        }
        
    return extracted_data


pathHTML = "html_files"  
pathJSON = "jsons"   

os.makedirs(pathJSON, exist_ok=True)


for file_name in os.listdir(pathHTML):
    if file_name.endswith('.html'):
        file_path = os.path.join(pathHTML, file_name)
        arxiv_id = file_name.split('.')[0] + "." + file_name.split(".")[1] 
        
        #Pases the html file to extract the information
        extracted_data = extract_elements_from_html(file_path)
        
        #Saves the information in a JSON file
        json_file_path = os.path.join(pathJSON, f"{arxiv_id}.json")
        with open(json_file_path, 'w', encoding='utf-8') as json_file:
            json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)

        print(f"File JSON created: {json_file_path}")

print(f"Finished. Path ---> '{pathJSON}'.")
