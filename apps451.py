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
# HEADER
# =========================================================

st.image("suto_logo.png", width=260)

st.title("SUTO S451 EX Flow Meter Sizing Tool")

st.markdown("""
Thermal Mass Flow Meter sizing calculator
based on SUTO S451 Manual.
""")

# =========================================================
# CONVERSION FACTOR
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
PIPE_MAP = {

    '1"': "DN25",
    '1-1/4"': "DN32",
    '1-1/2"': "DN40",
    '2"': "DN50",
    '2-1/2"': "DN65",
    '3"': "DN80",
    '4"': "DN100",
    '5"': "DN125",
    '6"': "DN150",
    '8"': "DN200",
    '10"': "DN250",
    '12"': "DN300",

}
# =========================================================
# FUNCTIONS
# =========================================================

def mmscfd_to_nm3h(flow):
    return flow * MMSCFD_TO_NM3H


def mmscfd_to_sm3h(flow):
    return flow * MMSCFD_TO_SM3H


def recommend_size(sm3h):

    for dn, data in S451_TABLE.items():

        if sm3h <= data["max_value"]:
            return dn, data

    return "Above DN300", None


# =========================================================
# SIDEBAR INPUT
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

# =========================================================
# FLOW INPUTS
# =========================================================

flow_min = st.sidebar.number_input(
    "Minimum Flow (MMSCFD)",
    min_value=0.0,
    value=1.0,
    step=0.1
)

flow_normal = st.sidebar.number_input(
    "Normal Flow (MMSCFD)",
    min_value=0.0,
    value=2.0,
    step=0.1
)

flow_max = st.sidebar.number_input(
    "Maximum / Upset Flow (MMSCFD)",
    min_value=0.0,
    value=3.0,
    step=0.1
)

# =========================================================
# PIPE CONNECTION OPTIONS
# =========================================================

st.sidebar.subheader("Pipe Connection Options")

pipe_option_1 = st.sidebar.text_input(
    "Option 1",
    '8"'
)

pipe_option_2 = st.sidebar.text_input(
    "Option 2",
    '10"'
)

pipe_option_3 = st.sidebar.text_input(
    "Option 3",
    '12"'
)

# =========================================================
# CALCULATION
# =========================================================

# MIN
nm3h_min = mmscfd_to_nm3h(flow_min)
sm3h_min = mmscfd_to_sm3h(flow_min)

# NORMAL
nm3h_normal = mmscfd_to_nm3h(flow_normal)
sm3h_normal = mmscfd_to_sm3h(flow_normal)

# MAX
nm3h_max = mmscfd_to_nm3h(flow_max)
sm3h_max = mmscfd_to_sm3h(flow_max)

# RECOMMENDATION
dn, data = recommend_size(sm3h_max)

# =========================================================
# RESULT
# =========================================================

st.header("Conversion Result")

result_df = pd.DataFrame({

    "Condition": [
        "MINIMUM",
        "NORMAL",
        "MAX / UPSET"
    ],

    "MMSCFD": [
        flow_min,
        flow_normal,
        flow_max
    ],

    "Nm3/h": [
        f"{nm3h_min:,.2f}",
        f"{nm3h_normal:,.2f}",
        f"{nm3h_max:,.2f}"
    ],

    "Sm3/h": [
        f"{sm3h_min:,.2f}",
        f"{sm3h_normal:,.2f}",
        f"{sm3h_max:,.2f}"
    ]

})

st.table(result_df)

st.success(f"Recommended S451 Size : {dn}")

st.header("Pipe Connection Options")

pipe_df = pd.DataFrame({

    "Option": [
        "Option 1",
        "Option 2",
        "Option 3"
    ],

    "Pipe Connection": [
        pipe_option_1,
        pipe_option_2,
        pipe_option_3
    ]
})

st.table(pipe_df)

st.header("Pipe Flow Range Comparison")

pipe_compare = []

pipe_options = [
    pipe_option_1,
    pipe_option_2,
    pipe_option_3
]

for pipe in pipe_options:

    if pipe in PIPE_MAP:

        dn_key = PIPE_MAP[pipe]

        pipe_data = S451_TABLE[dn_key]

        pipe_compare.append({

            "Pipe": pipe,
            "DN": dn_key,
            "Low Range": pipe_data["low"],
            "Standard Range": pipe_data["standard"],
            "Max Range": pipe_data["max"]

        })

compare_df = pd.DataFrame(pipe_compare)

st.table(compare_df)

# =========================================================
# FLOW RANGE
# =========================================================

if data is not None:

    st.header("S451 Flow Range")

    range_df = pd.DataFrame({

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

    st.table(range_df)

# =========================================================
# ACCESSORIES
# =========================================================

st.header("Accessories & Options")

acc_df = pd.DataFrame({

    "P/N": [
        "A530 1119",
        "A530 1120",
        "A1560",
        "A1558",
        "A1559",
        "A1565",
    ],

    "Description": [
        "High-pressure installation device",
        "High-pressure installation device",
        "Output Module",
        "Pressure Option",
        "Pressure Option",
        "Low Pressure Option",
    ],

    "Remark": [
        "200 mm shaft / >1.5 MPa",
        "300 mm shaft / >1.5 MPa",
        "2x4-20mA + Pulse + Modbus",
        "0 ... 1.6 MPa(g)",
        "0 ... 5.0 MPa(g)",
        "0 ... 0.2 MPa(g) Non-Ex",
    ]
})

st.table(acc_df)

# =========================================================
# ENGINEERING NOTES
# =========================================================

st.header("Engineering Notes")

st.info("""
Recommended operating range:
30% to 70% of max range.

Reference Conditions:

Sm3/h:
20°C, 1000 mbar (ISO1217)

Nm3/h:
0°C, 1013.25 mbar (DIN1343)

Avoid wet gas and condensate
for thermal mass flowmeters.

Recommended straight pipe:
20D - 50D upstream
5D downstream
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

    # =====================================================
    # LOGO
    # =====================================================

    logo = Image("suto_logo.png")

    logo.drawHeight = 60
    logo.drawWidth = 330
    logo.hAlign = 'CENTER'

    elements.append(logo)
    elements.append(Spacer(1, 25))

    # =====================================================
    # TITLE
    # =====================================================

    title_style = styles['Title']
    title_style.alignment = 1

    title = Paragraph(
        "SUTO S451 EX Flow Meter Sizing Report",
        title_style
    )

    elements.append(title)
    elements.append(Spacer(1, 20))

    # =====================================================
    # MAIN INFO
    # =====================================================

    info = [

        ["Project", project_name],
        ["Client", client_name],
        ["Gas Type", gas_type],

        ["Min Flow", f"{flow_min:.3f} MMSCFD"],
        ["Normal Flow", f"{flow_normal:.3f} MMSCFD"],
        ["Max/Upset Flow", f"{flow_max:.3f} MMSCFD"],

        ["Min Sm3/h", f"{sm3h_min:,.2f}"],
        ["Normal Sm3/h", f"{sm3h_normal:,.2f}"],
        ["Max Sm3/h", f"{sm3h_max:,.2f}"],

        ["Recommended Size", dn],

    ]

    table = Table(
        info,
        colWidths=[180, 250]
    )

    table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),

    ]))

    elements.append(table)

    elements.append(Spacer(1, 25))

    pipe_title = Paragraph(
        "Pipe Connection Options",
        styles['Heading2']
    )
    
    elements.append(pipe_title)
    
    pipe_data = [
    
        ["Option", "Pipe Connection"],
    
        ["Option 1", pipe_option_1],
        ["Option 2", pipe_option_2],
        ["Option 3", pipe_option_3],
    
    ]
    
    pipe_table = Table(
        pipe_data,
        colWidths=[180, 250]
    )
    
    pipe_table.setStyle(TableStyle([
    
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    
    ]))
    
    elements.append(pipe_table)

    elements.append(Spacer(1, 20))

    compare_title = Paragraph(
        "Pipe Flow Range Comparison",
        styles['Heading2']
    )
    
    elements.append(compare_title)
    
    compare_data = [
    
        ["Pipe", "DN", "Low", "Standard", "Max"]
    
    ]
    
    for pipe in [pipe_option_1, pipe_option_2, pipe_option_3]:
    
        if pipe in PIPE_MAP:
    
            dn_key = PIPE_MAP[pipe]
    
            pipe_data = S451_TABLE[dn_key]
    
            compare_data.append([
    
                pipe,
                dn_key,
                pipe_data["low"],
                pipe_data["standard"],
                pipe_data["max"]
    
            ])
    
    compare_table = Table(
        compare_data,
        colWidths=[60, 70, 120, 120, 120]
    )
    
    compare_table.setStyle(TableStyle([
    
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    
    ]))
    
    elements.append(compare_table)
    
    elements.append(Spacer(1, 25))

    # =====================================================
    # FLOW RANGE
    # =====================================================

    if data is not None:
        range_title = Paragraph(
            f"S451 Flow Range - Recommended Size {dn} ({data['inch']})",
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
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),

        ]))

        elements.append(range_table)

        elements.append(Spacer(1, 25))

    # =====================================================
    # ACCESSORIES
    # =====================================================

    accessories_title = Paragraph(
        "Accessories & Options",
        styles['Heading2']
    )

    elements.append(accessories_title)

    accessories_data = [

        ["P/N", "Description", "Remark"],

        [
            "A530 1119",
            "High-pressure installation device",
            "For 200 mm shaft / Pressure > 1.5 MPa"
        ],

        [
            "A530 1120",
            "High-pressure installation device",
            "For 300 mm shaft / Pressure > 1.5 MPa"
        ],

        [
            "A1560",
            "Output Module",
            "2 x 4-20 mA + Pulse + Modbus RTU"
        ],

        [
            "A1558",
            "Pressure Option",
            "0 ... 1.6 MPa(g)"
        ],

        [
            "A1559",
            "Pressure Option",
            "0 ... 5.0 MPa(g)"
        ],

        [
            "A1565",
            "Low Pressure Option",
            "0 ... 0.2 MPa(g) Non-Ex only"
        ],
    ]

    accessories_table = Table(
        accessories_data,
        colWidths=[90, 180, 220]
    )

    accessories_table.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),

    ]))

    elements.append(accessories_table)

    elements.append(Spacer(1, 25))

    # =====================================================
    # ENGINEERING NOTES
    # =====================================================

    notes = Paragraph(
        """
        <b>Engineering Notes</b><br/><br/>

        Recommended operating range:
        30% - 70% of maximum range.<br/><br/>

        <b>Reference Conditions</b><br/>
        Sm3/h = 20°C, 1000 mbar (ISO1217)<br/>
        Nm3/h = 0°C, 1013.25 mbar (DIN1343)<br/><br/>

        Avoid wet gas and condensate
        for thermal mass flowmeters.<br/><br/>

        Recommended straight pipe:<br/>
        Upstream: 20D - 50D<br/>
        Downstream: 5D
        """,
        styles['BodyText']
    )

    elements.append(notes)

    elements.append(Spacer(1, 25))

    # =====================================================
    # FOOTER
    # =====================================================

    footer = Paragraph(
        f"Generated: {datetime.now()}",
        styles['Italic']
    )

    elements.append(footer)

    # =====================================================
    # BUILD PDF
    # =====================================================

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
