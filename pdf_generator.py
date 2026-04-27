from fpdf import FPDF
import os

class OrderPDF(FPDF):
    def header(self):
        # Arial (standard) for header
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Exhibition Booth Order Summary', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def generate_order_pdf(order_data, filename="order_summary.pdf"):
    pdf = OrderPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Order details
    pdf.cell(200, 10, txt=f"Order ID: {order_data.get('order_id', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {order_data.get('date', 'N/A')}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Booth Specifications:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"- Dimensions: {order_data['length']}m x {order_data['width']}m", ln=True)
    pdf.cell(200, 10, txt=f"- Area: {order_data['length'] * order_data['width']} sq.m", ln=True)
    pdf.cell(200, 10, txt=f"- Construction: {order_data['construction_name']}", ln=True)
    
    materials_text = ", ".join(order_data['materials_names']) if order_data['materials_names'] else "None"
    pdf.cell(200, 10, txt=f"- Materials: {materials_text}", ln=True)
    
    equipment_text = ", ".join(order_data['equipment_names']) if order_data['equipment_names'] else "None"
    pdf.cell(200, 10, txt=f"- Equipment: {equipment_text}", ln=True)
    
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt=f"TOTAL PRICE: {order_data['total_price']:.2f} EUR", ln=True)
    
    pdf.output(filename)
    return filename
