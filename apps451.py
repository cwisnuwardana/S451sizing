import streamlit as st
import pandas as pd
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SUTO S451 EX Sizing Tool",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.image("suto_logo.png", width=220)
st.title("SUTO S451 EX Flow Meter Sizing Tool")

st.markdown("""
Thermal Mass Flow Meter sizing calculator
based on SUTO S451 Manual.
""")

# =========================================================
# CONSTANT
# =========================================================

MMSCFD_TO_NM3H = 1179.87
MMSCFD_TO_SM3H = 1253.00

# =========================================================
# S451 FLOW TABLE
# =========================================================

S451_TABLE = {
    "DN25": {
        "inch": '1"',
        "low": "0.2 ~ 48",
        "standard": "0.8 ~ 191",
        "max": "1.5 ~ 382",
        "max_value": 382
    },

    "DN32": {
        "inch": '1-1/4"',
        "low": "0.3 ~ 86",
        "standard": "1.4 ~ 345",
        "max": "2.8 ~ 689",
        "max_value": 689
    },

    "DN40": {
        "inch": '1-1/2"',
        "low": "0.5 ~ 119",
        "standard": "1.9 ~ 475",
        "max": "3.8 ~ 949",
        "max_value": 949
    },

    "DN50": {
        "inch": '2"',
        "low": "0.8 ~ 194",
        "standard": "3.1 ~ 777",
        "max": "6.2 ~ 1554",
        "max_value": 1554
    },

    "DN65": {
        "inch": '2-1/2"',
        "low": "1.3 ~ 332",
        "standard": "5.3 ~ 1329",
        "max": "10.6 ~ 2658",
        "max_value": 2658
    },

    "DN80": {
        "inch": '3"',
        "low": "1.8 ~ 461",
        "standard": "7.4 ~ 1843",
        "max": "14.7 ~ 3686",
        "max_value": 3686
    },

    "DN100": {
        "inch": '4"',
        "low": "2.8 ~ 707",
        "standard": "11.3 ~ 2826",
        "max": "23 ~ 5653",
        "max_value": 5653
    },

    "DN125": {
        "inch": '5"',
        "low": "4.4 ~ 1107",
        "standard": "17.7 ~ 4427",
        "max": "35 ~ 8853",
        "max_value": 8853
    },

    "DN150": {
        "inch": '6"',
        "low": "6.4 ~ 1596",
        "standard": "26 ~ 6382",
        "max": "51 ~ 12764",
        "max_value": 12764
    },

    "DN200": {
        "inch": '8"',
        "low": "11.4 ~ 2843",
        "standard": "45 ~ 11373",
        "max": "91 ~ 22746",
        "max_value": 22746
    },

    "DN250": {
        "inch": '10"',
        "low": "18 ~ 4448",
        "standard": "71 ~ 17791",
        "max": "142 ~ 35583",
        "max_value": 35583
    },

    "DN300": {
        "inch": '12"',
        "low": "26 ~ 6413",
        "standard": "103 ~ 25650",
        "max": "205 ~ 51300",
        "max_value": 51300
    }
}

# =========================================================
# FUNCTION
# =========================================================

def mmscfd_to_nm3h(flow):
    return flow * MMSCFD_TO_NM3H


def mmscfd_to_sm3h(flow):
    return flow * MMSCFD_TO_SM3H


def recommend_size(sm3h):

    for dn, data in S451_TABLE.items():

        if sm3h <= data["max_value"]:
            return dn, data

    return None, None


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("Input Data")

project_name = st.sidebar.text_input(
    "Project Name",
    "Project ABC"
)

client_name = st.sidebar.text_input(
    "Client Name",
    "Customer"
)

gas_type = st.sidebar.selectbox(
    "Gas Type",
    [
        "Air",
        "Nitrogen",
        "Natural Gas",
        "Oxygen",
        "Hydrogen",
        "CO2"
    ]
)

flow = st.sidebar.number_input(
    "Flow (MMSCFD)",
    min_value=0.0,
    value=2.0,
    step=0.1
)

# =========================================================
# CALCULATION
# =========================================================

nm3h = mmscfd_to_nm3h(flow)
sm3h = mmscfd_to_sm3h(flow)

dn, data = recommend_size(sm3h)

# =========================================================
# RESULT
# =========================================================

st.header("Conversion Result")

col1, col2, col3 = st.columns(3)

col1.metric("Nm³/h", f"{nm3h:,.2f}")
col2.metric("Sm³/h", f"{sm3h:,.2f}")

if dn:
    col3.metric("Recommended Size", dn)
else:
    col3.metric("Recommended Size", "Above DN300")

# =========================================================
# RANGE TABLE
# =========================================================

if dn:

    st.header("S451 Flow Range")

    df = pd.DataFrame({
        "Range Type": [
            "LOW RANGE",
            "STANDARD RANGE",
            "MAX RANGE"
        ],

        "Flow Range (Sm3/h)": [
            data["low"],
            data["standard"],
            data["max"]
        ]
    })

    st.table(df)

# =========================================================
# ENGINEERING NOTES
# =========================================================

st.header("Engineering Notes")

st.info("""
Recommended operating range is around
30% to 70% of max flow range.

Reference Conditions:

Sm3/h:
20°C, 1000 mbar (ISO1217)

Nm3/h:
0°C, 1013.25 mbar (DIN1343)

Avoid wet gas and condensate for
thermal mass flow measurement.
""")

# =========================================================
# PDF GENERATOR
# =========================================================

def generate_pdf():

    filename = "S451_Sizing_Report.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    elements = []

    logo = Image("suto_logo.png")

    logo.drawHeight = 60
    logo.drawWidth = 330

    elements.append(logo)
    elements.append(Spacer(1, 20))
    
    title = Paragraph(
        "SUTO S451 EX Flow Meter Sizing Report",
        styles['Title']
    )

    elements.append(title)
    elements.append(Spacer(1, 12))

    info = [
        ["Project", project_name],
        ["Client", client_name],
        ["Gas Type", gas_type],
        ["Input Flow", f"{flow:.3f} MMSCFD"],
        ["Nm3/h", f"{nm3h:,.2f}"],
        ["Sm3/h", f"{sm3h:,.2f}"],
        ["Recommended Size", dn],
    ]

    table = Table(info, colWidths=[180, 250])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))

    elements.append(table)

    elements.append(Spacer(1, 20))

    range_title = Paragraph(
        "S451 Flow Range",
        styles['Heading2']
    )

    elements.append(range_title)

    range_data = [
        ["Range", "Flow (Sm3/h)"],
        ["LOW RANGE", data["low"]],
        ["STANDARD RANGE", data["standard"]],
        ["MAX RANGE", data["max"]],
    ]

    range_table = Table(
        range_data,
        colWidths=[180, 250]
    )

    range_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))

    elements.append(range_table)

    elements.append(Spacer(1, 20))

    notes = Paragraph(
        """
        <b>Reference Conditions</b><br/>
        Sm3/h = 20°C, 1000 mbar (ISO1217)<br/>
        Nm3/h = 0°C, 1013.25 mbar (DIN1343)<br/><br/>

        Recommended operation:
        30% - 70% of maximum range.<br/><br/>

        Avoid wet gas and condensate for thermal
        mass flow applications.
        """,
        styles['BodyText']
    )

    elements.append(notes)

    elements.append(Spacer(1, 20))

    footer = Paragraph(
        f"Generated: {datetime.now()}",
        styles['Italic']
    )

    elements.append(footer)

    doc.build(elements)

    return filename

# =========================================================
# DOWNLOAD PDF
# =========================================================

if st.button("Generate PDF Report"):

    pdf_file = generate_pdf()

    with open(pdf_file, "rb") as f:

        st.download_button(
            label="Download PDF",
            data=f,
            file_name=pdf_file,
            mime="application/pdf"
        )
