from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import LongTable, Paragraph, SimpleDocTemplate, Spacer


def build_pdf(output, transactions, summary):
    document = SimpleDocTemplate(output, pagesize=A4, title="Expense report")
    styles = getSampleStyleSheet()
    rows = [["Date", "Type", "Category", "Amount (INR)", "Description"]]

    for transaction in transactions.iterator(chunk_size=500):
        rows.append(
            [
                transaction.date.isoformat(),
                transaction.kind,
                Paragraph(escape(transaction.category.name), styles["BodyText"]),
                f"{transaction.amount:.2f}",
                Paragraph(escape(transaction.description), styles["BodyText"]),
            ]
        )
    table_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#183044")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (3, 1), (3, -1), "RIGHT"),
        ("LINEBELOW", (0, 0), (-1, -1), 0.25, colors.lightgrey),
    ]
    if len(rows) == 1:
        rows.append(["No transactions match.", "", "", "", ""])
        table_style.append(("SPAN", (0, 1), (-1, 1)))

    table = LongTable(
        rows,
        colWidths=[69, 49, 92, 77, document.width - 287],
        repeatRows=1,
        style=table_style,
    )
    document.build(
        [
            Paragraph("Expense report", styles["Title"]),
            Paragraph(
                f"Income: {summary['income']:.2f} INR &nbsp; "
                f"Expenses: {summary['expense']:.2f} INR &nbsp; Balance: {summary['balance']:.2f} INR",
                styles["BodyText"],
            ),
            Spacer(1, 12),
            table,
        ]
    )
