import os
import markdown
from bs4 import BeautifulSoup
from fpdf import FPDF
import webbrowser
from agent.logging import log
from pprint import pprint

class PDF(FPDF):
    def __init__(self):
        super().__init__()
        
        self.add_font('DejaVu', '', 'fonts/DejaVuSans.ttf', uni=True)
        self.add_font('DejaVu', 'B', 'fonts/DejaVuSans-Bold.ttf', uni=True)
        self.add_font('DejaVu', 'I', 'fonts/DejaVuSans-Oblique.ttf', uni=True)
        self.add_font('DejaVu', 'BI', 'fonts/DejaVuSans-BoldOblique.ttf', uni=True)
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()

    def header(self):
        self.set_font('DejaVu', 'B', 10)
        self.cell(0, 10, 'Z47 | Company Briefing', align='L')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', 'I', 8)
        self.cell(0, 10, 'Confidential', align='L')
        self.cell(0, 10, f'Page {self.page_no()}', align='R')

    def write_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        pprint(soup)
        for element in soup.children:
            self._render_element(element)

    def _render_element(self, element):
        if element.name is None:
            text = element.string.strip()
            if text:
                self.set_font("DejaVu", '', 10)
                self.multi_cell(0, 6, text)
            return

        if element.name.startswith('h'):
            if len(element.name) > 1 and element.name[1].isdigit():  # Check if the second character is a digit
                level = int(element.name[1])
                size = 14 - level  # reduced size
                self.set_font("DejaVu", 'B', size)
                self.ln(2)
                self.multi_cell(0, 7, element.get_text(strip=True))
                self.ln(1)
            else:
                log(f"Unexpected header format: {element.name}")  # Log unexpected header formats

        elif element.name == 'p':
            self.set_font("DejaVu", '', 10)
            self._render_inline(element)
            self.ln(3)

        elif element.name in ['strong', 'b']:
            self.set_font("DejaVu", 'B', 10)
            self.write(5, element.get_text())

        elif element.name in ['em', 'i']:
            self.set_font("DejaVu", 'I', 10)
            self.write(5, element.get_text())

        elif element.name == 'a':
            self.set_text_color(0, 0, 255)
            self.set_font("DejaVu", 'U', 10)
            self.write(5, element.get_text(), element.get('href'))
            self.set_text_color(0, 0, 0)

        

        elif element.name == 'ul':
            for li in element.find_all('li', recursive=False):
                self.set_font("DejaVu", '', 10)
                self.cell(5)
                self.write(5, u"\u2022 ")
                self._render_inline(li)
                self.ln(6)  # Space between bullets

        elif element.name == 'ol':
            for i, li in enumerate(element.find_all('li', recursive=False), start=1):
                self.set_font("DejaVu", '', 10)
                self.cell(5)
                self.write(5, f"{i}. ")
                self._render_inline(li)
                self.ln(6)

        elif element.name == 'blockquote':
            self.set_font("DejaVu", 'I', 10)
            self.set_text_color(100, 100, 100)
            self.multi_cell(0, 6, f"“{element.get_text(strip=True)}”")
            self.set_text_color(0, 0, 0)
            self.ln(2)

        elif element.name == 'code':
            self.set_font("Courier", '', 9)
            self.set_fill_color(240, 240, 240)
            self.multi_cell(0, 6, element.get_text(strip=True), fill=True)
            self.set_fill_color(255, 255, 255)
            self.ln(2)

        elif element.name == 'li':
            self.set_font("DejaVu", '', 10)
            self.cell(5)  # Indentation for list items
            self._render_inline(element)  # Process inline elements within the list item
            self.ln(6)  # Space between list items

        else:
            self._render_inline(element)

    def _render_inline(self, element):
        for child in element.children:
            if child.name is None:
                text = child.string or ''
                self.set_font("DejaVu", '', 10)
                self.write(5, text)
            elif child.name in ['strong', 'b']:
                self.set_font("DejaVu", 'B', 10)
                self.write(5, child.get_text())
                self.set_font("DejaVu", '', 10)  # Reset to normal
            elif child.name in ['em', 'i']:
                self.set_font("DejaVu", 'I', 10)
                self.write(5, child.get_text())
                self.set_font("DejaVu", '', 10)
            elif child.name == 'a':
                href = child.get('href')
                text = child.get_text()
                self.set_text_color(0, 0, 255)
                self.set_font("DejaVu", '', 10)
                self.write(5, text, href)
                self.set_text_color(0, 0, 0)
            elif child.name == 'code':
                self.set_font("Courier", '', 9)
                self.set_fill_color(240, 240, 240)
                self.write(5, child.get_text())
                self.set_fill_color(255, 255, 255)
                self.set_font("DejaVu", '', 10)
            else:
                self._render_element(child)


def convert_markdown_to_pdf(md_text, filename):
    log("Generating PDF...", tag="INFO")
    html = markdown.markdown(md_text)

    try:
        pdf = PDF()
        pdf.write_html(html)

        os.makedirs(os.path.dirname(filename), exist_ok=True)
        pdf.output(filename)
        webbrowser.open(f'file://{os.path.abspath(filename)}')
        log("PDF generated successfully", tag="SUCCESS")
        return filename
    except Exception as e:
        log(f"PDF generation failed: {str(e)}", tag="ERROR")
        return None
