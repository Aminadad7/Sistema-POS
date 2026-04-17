from datetime import datetime
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from app.utils.constants import BASE_DIR


INVOICE_FOLDER = BASE_DIR / 'invoices'
INVOICE_FOLDER.mkdir(parents=True, exist_ok=True)


def generate_invoice_pdf(invoice_data: dict, filename: str | None = None) -> str:
    client_name = invoice_data.get('client_name', 'Consumidor Final').strip() or 'Consumidor Final'
    safe_client = ''.join(
        ch for ch in client_name.lower().replace(' ', '_')
        if ch.isalnum() or ch in ('_', '-')
    ) or 'consumidor_final'
    invoice_number = invoice_data.get('invoice_number', datetime.utcnow().strftime('FAC%Y%m%d%H%M%S'))

    if filename is None:
        filename = f'{safe_client}_{invoice_number}.pdf'

    file_path = INVOICE_FOLDER / filename
    suffix = 1
    while file_path.exists():
        file_path = INVOICE_FOLDER / f'{safe_client}_{invoice_number}_{suffix}.pdf'
        suffix += 1

    document = SimpleDocTemplate(
        str(file_path),
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    stylesheet = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=stylesheet['Heading1'],
        alignment=1,
        fontSize=20,
        textColor=colors.black,
        leading=24,
        spaceAfter=8,
    )
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=stylesheet['Heading2'],
        fontSize=14,
        textColor=colors.black,
        leading=18,
        spaceAfter=6,
    )
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=stylesheet['Normal'],
        fontSize=12,
        textColor=colors.black,
        leading=16,
    )
    contact_style = ParagraphStyle(
        'ContactStyle',
        parent=stylesheet['Normal'],
        fontSize=11,
        textColor=colors.black,
        leading=14,
        alignment=1,
        italic=True,
        spaceAfter=2,
    )

    story = []
    logo_path = invoice_data.get('business_logo_path', '')
    logo_table_data = []
    if logo_path:
        logo_file = Path(logo_path)
        if logo_file.exists():
            try:
                logo_image = Image(str(logo_file), width=80, height=80)
                business_info = [
                    Paragraph(invoice_data.get('business_name', 'Mi Negocio'), title_style)
                ]
                if invoice_data.get('business_address'):
                    business_info.append(Paragraph(invoice_data.get('business_address'), contact_style))
                if invoice_data.get('business_phone'):
                    business_info.append(Paragraph(f'Teléfono: {invoice_data.get("business_phone")}', contact_style))
                logo_table_data.append([logo_image, business_info])
            except Exception:
                logo_table_data = []
    if logo_table_data:
        logo_table = Table(logo_table_data, colWidths=[90, 400])
        logo_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ]))
        story.append(logo_table)
    else:
        story.append(Paragraph(invoice_data.get('business_name', 'Mi Negocio'), title_style))
        if invoice_data.get('business_address'):
            story.append(Paragraph(invoice_data.get('business_address'), contact_style))
        if invoice_data.get('business_phone'):
            story.append(Paragraph(f'Teléfono: {invoice_data.get("business_phone")}', contact_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph('Factura', header_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f'Nº de factura: {invoice_number}', normal_style))
    story.append(Paragraph(f'Fecha: {invoice_data.get("date", datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"))}', normal_style))
    story.append(Paragraph(f'Cliente: {client_name}', normal_style))
    story.append(Spacer(1, 16))

    table_data = [['Producto', 'Cantidad', 'Precio unitario', 'Total']]
    for item in invoice_data.get('items', []):
        table_data.append([
            item['name'],
            str(item['quantity']),
            f"{item['unit_price']:.2f}",
            f"{item['total_price']:.2f}",
        ])

    invoice_table = Table(table_data, colWidths=[220, 80, 100, 100])
    invoice_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(invoice_table)
    story.append(Spacer(1, 18))

    summary_data = [
        ['Subtotal:', f"{invoice_data.get('subtotal', 0):.2f}"],
        ['Descuento:', f"{invoice_data.get('discount', 0):.2f}"],
        ['ITBIS:', f"{invoice_data.get('tax', 0):.2f}"],
        ['Total:', f"{invoice_data.get('total', 0):.2f}"],
        ['Pagado:', f"{invoice_data.get('paid_amount', 0):.2f}"],
        ['Cambio:', f"{invoice_data.get('change_amount', 0):.2f}"],
    ]
    summary_table = Table(summary_data, colWidths=[280, 120])
    summary_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 20))
    story.append(Paragraph('Gracias por su compra.', normal_style))

    document.build(story)
    return str(file_path)
