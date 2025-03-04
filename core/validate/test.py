from PyPDF2 import PdfReader

def pdf_to_image_pypdf2(pdf_path, output_folder='output_images'):
    if pdf_path.endswith('.pdf'):
         
          with open(pdf_path, 'rb') as file:
               reader = PdfReader(file)
               for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    xobject = page['/Resources']['/XObject'].get_object()  # Updated line
                    for obj in xobject:
                         if xobject[obj]['/Subtype'] == '/Image':
                              image_data = xobject[obj]._data
                              with open(f"{output_folder}/page_{page_num+1}.jpg", 'wb') as image_file:
                                   image_file.write(image_data)
                              
    if pdf_path.endswith(('.jpg', '.jpeg', '.png')):
          pass
                        