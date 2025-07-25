from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

def generate_pdf_bill(booking, cart_items, total_price):
    buffer = BytesIO()

    # --- Font Config ---
    FONT_TITLE = "Helvetica-Bold"
    SIZE_TITLE = 10
    FONT_SUBTITLE = "Helvetica-Oblique"
    SIZE_SUBTITLE = 8
    FONT_INFO = "Helvetica"
    SIZE_INFO = 7
    FONT_HEADER = "Helvetica-Bold"
    SIZE_HEADER = 6.5
    FONT_ITEM = "Helvetica"
    SIZE_ITEM = 6.5
    FONT_PRICE = "Courier"

    # --- Spacing ---
    LINE_SPACING_TITLE = 14
    LINE_SPACING_SUBTITLE = 12
    LINE_SPACING_INFO = 10
    LINE_SPACING_HEADER = 12
    LINE_SPACING_ITEM = 9
    SECTION_GAP = 6
    TOTAL_GAP = 10
    BOTTOM_EXTRA_MARGIN = 8 * mm

    # --- Page Setup ---
    receipt_width = 58 * mm
    side_margin = 3 * mm

    # --- Estimate Height ---
    content_height = (
        LINE_SPACING_TITLE +
        LINE_SPACING_SUBTITLE +
        4 * LINE_SPACING_INFO +
        SECTION_GAP +
        LINE_SPACING_HEADER + 2 +
        len(cart_items) * LINE_SPACING_ITEM +
        TOTAL_GAP +                   # Gap before total
        LINE_SPACING_HEADER +         # Total
        SECTION_GAP + LINE_SPACING_INFO +  # Gap + payment line
        BOTTOM_EXTRA_MARGIN
    )
    receipt_height = content_height

    p = canvas.Canvas(buffer, pagesize=(receipt_width, receipt_height))
    width, height = receipt_width, receipt_height
    y = height

    # --- Column Positions ---
    x_col1 = side_margin
    x_col2 = width * 0.6
    x_col3 = width - side_margin

    # --- Title ---
    p.setFont(FONT_TITLE, SIZE_TITLE)
    y -= LINE_SPACING_TITLE
    p.drawCentredString(width / 2, y, "Order Bill")

    p.setFont(FONT_SUBTITLE, SIZE_SUBTITLE)
    y -= LINE_SPACING_SUBTITLE
    p.drawCentredString(width / 2, y, "AHUF CAFE")

    # --- Booking Info ---
    y -= LINE_SPACING_INFO
    p.setFont(FONT_INFO, SIZE_INFO)
    y -= LINE_SPACING_INFO
    p.drawString(x_col1, y, f"Booking ID: {booking.id}")
    y -= LINE_SPACING_INFO
    p.drawString(x_col1, y, f"Customer Name: {booking.name}")
    y -= LINE_SPACING_INFO
    p.drawString(x_col1, y, f"Takeaway: {'Yes' if booking.is_takeaway else 'No'}")
    y -= LINE_SPACING_INFO
    p.drawString(x_col1, y, f"Payment: {booking.bill.payment_method}")
    y -= SECTION_GAP
    y -= LINE_SPACING_INFO
    # --- Table Header ---
    p.setFont(FONT_HEADER, SIZE_HEADER)
    p.drawString(x_col1, y, "Item")
    p.drawCentredString(x_col2, y, "Qty")
    p.drawRightString(x_col3, y, "Price")
    y -= 2
    p.line(x_col1, y, width - side_margin, y)
    y -= (LINE_SPACING_HEADER - 2)

    # --- Cart Items ---
    for item in cart_items:
        plate_desc = item.plate_option.plate_type.capitalize() if item.plate_option else "N/A"
        item_name = f"{item.menu_item.name} ({plate_desc})"
        total_item_price = item.quantity * item.price
        max_len = 28
        trimmed_name = (item_name[:max_len - 3] + '...') if len(item_name) > max_len else item_name

        p.setFont(FONT_ITEM, SIZE_ITEM)
        p.drawString(x_col1, y, f"• {trimmed_name}")
        p.drawCentredString(x_col2, y, f"x{item.quantity}")
        p.setFont(FONT_PRICE, SIZE_ITEM)
        p.drawRightString(x_col3, y, f"Rs.{total_item_price:.1f}")
        y -= LINE_SPACING_ITEM

    # --- Total Section ---
    y -= TOTAL_GAP
    p.line(x_col1, y, width - side_margin, y)
    y -= LINE_SPACING_HEADER

    p.setFont(FONT_HEADER, SIZE_HEADER + 1)
    p.drawString(x_col1, y, "Total")
    p.setFont(FONT_PRICE, SIZE_HEADER + 1)
    p.drawRightString(x_col3, y, f"Rs.{total_price:.1f}")

    # --- Payment Method at Bottom ---
    # y -= SECTION_GAP
    # y -= LINE_SPACING_INFO
    # p.setFont(FONT_INFO, SIZE_INFO)
    # p.drawString(x_col1, y, f"Paid by: {booking.bill.payment_method}")
    # y -= LINE_SPACING_INFO
    # y -= LINE_SPACING_INFO
    # y -= LINE_SPACING_INFO

    # Finalize
    p.save()
    buffer.seek(0)
    return buffer























