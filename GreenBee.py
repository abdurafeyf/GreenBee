import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import numpy as np
from fpdf import FPDF
import fpdf

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db

# cred_obj = credentials.Certificate("greenbee-servicekey.json")
# databaseURL = 'https://greenbee-project-default-rtdb.firebaseio.com/'

# try:
#     default_app = firebase_admin.initialize_app(cred_obj, {
# 	'databaseURL':databaseURL
# 	})
# except:
#     pass
# ref = db.reference("/")

st.title('GreenBee Innovation')

# Initialization
if 'key' not in st.session_state:
    st.session_state['key'] = 0



@st.cache(allow_output_mutation=True)
def get_dataframe():
    return pd.DataFrame(
        [("", 0, 0, 0, 0, 0)] * 50,
        columns=('Equipment Name', 'No', 'Watt', 'Using Hr', 'Total Watt', 'Watt Hr/Day'))


df = get_dataframe()


# Create row, column, and value inputs
equip_placeholder = st.empty()
no_placeholder = st.empty()
watt_placeholder = st.empty()
usinghr_placeholder = st.empty()
equip_name = equip_placeholder.text_input(
    label='Equipment Name', value="", key=0)
no = no_placeholder.number_input('No', value=0, key=1)
watt = watt_placeholder.number_input('Watt', value=0, key=2)
usinghr = usinghr_placeholder.number_input('Using Hr', value=0, key=3)

# Adding button and adding the data entered to the pandas dataframe
if st.button('Add'):
    df['Equipment Name'][st.session_state.key] = equip_name
    df['No'][st.session_state.key] = no
    df['Watt'][st.session_state.key] = watt
    df['Using Hr'][st.session_state.key] = usinghr

    df['Total Watt'][st.session_state.key] = df['No'][st.session_state.key] * \
        df['Watt'][st.session_state.key]

    df['Watt Hr/Day'][st.session_state.key] = df['No'][st.session_state.key] * \
        df['Watt'][st.session_state.key] * df['Using Hr'][st.session_state.key]
    st.session_state.key += 1
    equip_name = equip_placeholder.text_input(
        label='Equipment Name', value="", key=4)
    no = no_placeholder.number_input('No', value=0, key=5)
    watt = watt_placeholder.number_input('Watt', value=0, key=6)
    usinghr = usinghr_placeholder.number_input('Using Hr', value=0, key=7)


totalwattsum = df['Total Watt'].sum()
watthrsum = df['Watt Hr/Day'].sum()
# json_obj = {
#     'Load Details':
#         {
#             'totalwattsum': totalwattsum,
#             'watthrsum': watthrsum
#         }
#     }

# ref.set(json_obj)

st.subheader('Result')
st.write(f"Total Watt: {totalwattsum}")
st.write(f"Total Watt Hr/Day: {watthrsum}")

st.subheader('Entered Wrong Data? Delete it right away')
row_to_delete = st.text_input(
    label='Row to delete', placeholder='Enter number of row to be deleted')
if st.button(label='Delete row'):
    totalwattsum -= df['Total Watt'][int(row_to_delete)]
    watthrsum -= df['Watt Hr/Day'][int(row_to_delete)]
    # json_obj = {
    # 'Load Details':
    #     {
    #         'totalwattsum': totalwattsum,
    #         'watthrsum': watthrsum
    #     }
    # }

    # ref.set(json_obj)
    df['Equipment Name'][int(row_to_delete)] = ""
    df['No'][int(row_to_delete)] = 0
    df['Watt'][int(row_to_delete)] = 0
    df['Using Hr'][int(row_to_delete)] = 0
    df['Total Watt'][int(row_to_delete)] = 0
    df['Watt Hr/Day'][int(row_to_delete)] = 0
    st.session_state.key -= 1
st.write("or")
if st.button(label="Delete All Rows"):
    for i in range(len(df)):
        df['Equipment Name'][i] = ""
        df['No'][i] = 0
        df['Watt'][i] = 0
        df['Total Watt'][i] = 0
        df['Using Hr'][i] = 0
        df['Watt Hr/Day'][i] = 0
        st.session_state.key -= 1
st.subheader('Electrical Load Data')
# And display the result!
st.dataframe(df)
if st.button('Generate Graph'):
    st.area_chart(df, x='Total Watt', y='Watt Hr/Day')

    # st.set_option('deprecation.showPyplotGlobalUse', False)
    # totalwattgraph = [i for i in df['Total Watt']]
    # watthrdaygraph = [i for i in df['Watt Hr/Day']]

    # plt.fill_between(np.arange(12), totalwattgraph, color="lightpink",
    #                  alpha=0.5, label='Total Watt')
    # plt.fill_between(np.arange(12), watthrdaygraph, color="skyblue",
    #                  alpha=0.5, label='Watt Hr/Day')
    # st.pyplot(plt.show())

# from firebase_admin import db

# ref = db.reference("/Load Details/")

# totalwattsum = ref.order_by_child("totalwttsum".get())
# watthrsum = ref.order_by_child("watthrsum".get())
st.title("SOLAR PANEL CALCULATOR")
st.subheader("Solar Panel Details")
solar_sys_volt = st.number_input(label='Solar System Voltage (Volts DC)',
                                 value=24.0)
losses_in_wire = st.number_input(
    label='Losses in Wire, Connection, Battery (%)', value=20.0)
st.write('''
    ###### Daily Sunshine Hours
''')
with st.form(key='daily_sunshine_hr'):
    c1, c2, c3 = st.columns(3)
    with c1:
        inwinter = st.number_input("In Winter", value=5.0)
    with c2:
        insummer = st.number_input("In Summer", value=6.0)
    with c3:
        inmonsoon = st.number_input("In Monsoon", value=5.0)
    submitbtn = st.form_submit_button(label='Submit')

avg_sunshine = (inwinter+insummer+inmonsoon)/3
st.write(f"Average Daily Sunshine Hours: {round(avg_sunshine, 2)}")

st.write(f"Total Solar Power Need: {watthrsum}")

solar_power_correction = watthrsum + (watthrsum * (losses_in_wire/100))
st.write(
    f"Total Solar Power after correction factor: {solar_power_correction}")

solar_arr_size = solar_power_correction / avg_sunshine
st.write(f"Solar array size after calculating Sun Hour: {solar_arr_size}")

st.write('''
    ###### Size of Solar Panel
''')
with st.form('sizeofsolarpanel'):
    c1, c2 = st.columns(2)
    with c1:
        sizeofpanelwatt = st.number_input(label='Watts (W)', value=420.0)
    with c2:
        sizeofpanelvolt = st.number_input(label='Volts (V)', value=24.0)
    sizebtn = st.form_submit_button(label='Done')
solarpanel_conn = st.selectbox(
    label='Solar Panel Connection',
    options=('Parallel', 'Series', 'Series-Parallel'),
    index=0
)

st.subheader('Output of Solar Panel')
st.write(
    f'''
    ###### Size of solar panel: 
    {sizeofpanelwatt} Watt, {sizeofpanelvolt} Volts
    ''')

st.write(
    f'''
    ###### Type of connection for Solar Panel: 
    {solarpanel_conn}
    ''')

# losses_in_wire = st.number_input(
#     label='Losses in Wire, Connection, Battery (%)', value=20.0)

st.write(
    '''
    ###### Selection of Solar Panel Connection criteria: 
    ''')
ok = True
if(solarpanel_conn == 'Series'):
    x = 1
    if(sizeofpanelwatt >= solar_arr_size):
        st.write('OK')
        y = 1
        ok = True
    else:
        st.write('Select Other Type of Connection')
        y = 0
        ok = False

elif(solarpanel_conn == 'Parallel'):
    x = 2
    if(sizeofpanelwatt >= solar_sys_volt):
        st.write('OK')
        y = 1
        ok = True
    else:
        st.write('Select Other Type of Connection')
        y = 0
        ok = False

elif(solarpanel_conn == 'Series-Parallel'):
    x = 3
    if(sizeofpanelwatt < solar_arr_size):
        if(sizeofpanelwatt < solar_sys_volt):
            st.write('OK')
            y = 1
            ok = True
        else:
            st.write('Select Other Type of Connection')
            y = 0
            ok = False
    else:
        st.write('Select Other Type of Connection')
        y = 0
        ok = False
else:
    st.write('')

ok_eff = True
if((solar_sys_volt % sizeofpanelvolt) == 0):
    st.write(
        '''
        ###### Selection of each solar panel efficiency: 
        OK
        ''')
    ok_eff = True
else:
    st.write(
        f'''
        ###### Selection of each solar panel efficiency: 
        Select other solar voltage instead of {sizeofpanelvolt} volts''')
    ok_eff = False


amphr = round(((solar_arr_size)/(sizeofpanelwatt)), 1)

st.write('''
    ###### Number of string for solar panel: 
    ''')
z = 0
if(y == 0):
    st.write('')
else:
    if(x == 1):
        z = 1
        st.write(f'{z}')
    elif(x == 2):
        z = round((amphr+0.1))
        st.write(f'{z}')
    elif(x == 3):
        z = round((amphr+0.1))
        st.write(f'{z}')
    else:
        st.write('')


st.write('''
    ###### Total watt of each solar panel string: 
    ''')
if(y == 1):
    st.write(f'{sizeofpanelwatt} watt, {(sizeofpanelwatt)/(sizeofpanelvolt)} amp')
else:
    st.write('')


st.write(
    '''
    ###### Total No. of Solar Panel in each string: 
    ''')

if((solar_sys_volt % sizeofpanelvolt) == 0):
    solarpanelineachstring = (solar_sys_volt)/(sizeofpanelvolt)
    st.write(f'{solarpanelineachstring}')
else:
    st.write('')

t = z*sizeofpanelwatt

st.subheader('Total Watts of Solar Panel: ')
st.write(f'{t} watts, {t/sizeofpanelvolt} amps')


st.subheader('Total no. of Solar Panel: ')
st.write(f'{z*solarpanelineachstring}')
# from firebase_admin import db

# ref = db.reference("/Load Details/")

# totalwattsum = ref.order_by_child("totalwttsum".get())
# watthrsum = ref.order_by_child("watthrsum".get())
st.title('BATTERY BANK CALCULATOR')
st.subheader("Battery Bank Load Details")

bttry_bank_volt = st.number_input(
    label='Battery Bank\'s Voltage: (Volts DC)', value=24)
rsrv_day = st.number_input(
    label='Reserve days (No. of days battery gives current)', value=15)
loss = st.number_input(
    label='Loose connection / Wire loss factor (%)', value=20)
bttry_eff = st.number_input(label='Battery Effeciency (%)', value=100)
bttry_aging = st.number_input(label='Battery Aging (%)', value=100)
dod = st.number_input(label='Depth of discharge (%)', value=50)

with st.form('temp'):
    c1, c2 = st.columns(2)
    with c1:
        temperature = st.number_input(
            label='Battery Operating Temperature ', value=80)
    with c2:
        temp_unit = st.selectbox(
            label='Temperature Units',
            options=('C', 'F'),
            index=0,
            label_visibility='hidden'
        )
    st.form_submit_button('Submit')

# THE BATTERY BANK REQUIRED

st.write('''
    ###### Each Battery Rating
''')
with st.form('eachbatteryrating'):
    c1, c2 = st.columns(2)
    with c1:
        bttry_rating_amphr = st.number_input(
            label='Ampere-Hour (Amp.Hr)', value=150.0)
    with c2:
        bttry_rating_volts = st.number_input(label='Volts (V)', value=12.0)
    sizebtn = st.form_submit_button(label='Done')

battery_conn = st.selectbox(
    label='Batteries connection for battery bank',
    options=('Parallel', 'Series', 'Series-Parallel'),
    index=0
)


st.subheader('Battery Bank Output')
st.write(f'Type of connection for Batteries: {battery_conn}')


st.subheader('Battery Calculations')

st.write(f'Total KW.Hr/Day : {watthrsum} Watt.Hr/Day')

total_amphr = watthrsum / bttry_bank_volt
st.write(f'Total Amp.Hr : {total_amphr} Amp.Hr')

avg_load = (total_amphr * (1 + (loss / 100))) / (bttry_eff / 100)
st.write(f'Average Load : {avg_load} Amp.Hr')

storage_req = avg_load * rsrv_day
st.write(f'Storage Required : {storage_req} Amp.Hr')

battery_aging = (storage_req) * (1+(bttry_aging/100))
st.write(f'Battery aging : {battery_aging} Amp.Hr')

pdf = FPDF()
 
pdf.add_page()

pdf.image(name='profile2.jpeg', w=150, h=100, x=30)
pdf.ln(h=20)
pdf.set_font("Times", "B",size = 30)
 

pdf.cell(200, 10, txt = "GreenBee Innovation & Energy",
         ln = 1, align = 'C')

pdf.set_font("Arial",size = 20)

pdf.cell(200, 10, txt = "Electrical Details Report",
         ln = 2, align = 'C')
pdf.set_font("Times", "B", size = 15)
pdf.cell(200, 10, txt = "Output of Solar Panel", ln = 3, align = 'L')

pdf.set_font("Arial", size = 13)
pdf.cell(200, 10, txt = f"Size of Solar Panel: {sizeofpanelwatt} Watt, {sizeofpanelvolt} Volts", ln=4)

pdf.cell(200, 10, txt = f"Type of connection for solar panel: {solarpanel_conn}", ln = 5)

if ok == True:
    pdf.cell(200, 10, txt = f"Selection of Solar Panel Connection Criteria: OK", ln=6)
else:
    pdf.cell(200, 10, txt = f"Selection of Solar Panel Connection Criteria: Select other type of connection", ln=6)

if ok_eff == True:
    pdf.cell(200, 10, txt = f"Selection of Solar Panel efficiency: OK", ln=7)
else:
    pdf.cell(200, 10, txt = f"Selection of Solar Panel efficiency: Select other solar voltage instead of {sizeofpanelvolt} volts", ln=7)

pdf.cell(200, 10, txt = f"Number of string for solar panel: {z}", ln=8)

if y == 1:
    pdf.cell(200, 10, txt = f"Total watt of each solar panel string: {sizeofpanelwatt} watt, {(sizeofpanelwatt)/(sizeofpanelvolt)} amp", ln=9)
else:
    pdf.cell(200, 10, txt="", ln=9)

if((solar_sys_volt % sizeofpanelvolt) == 0):
    pdf.cell(200, 10, txt = f"Total No. of Solar Panel in each string: {solarpanelineachstring}", ln=10)
else:
    pdf.cell(200, 10, txt = "", ln=10)
    
pdf.cell(200, 10, txt = f"Total Watts of Solar Panel: {t} watts, {round(t/sizeofpanelvolt, 2)} amps", ln=11)

pdf.cell(200, 10, txt = f"Total No. of Solar Panel: {z*solarpanelineachstring}")

with st.sidebar:
    st.image(image='profile2.jpeg')
    if st.download_button('Generate PDF'):
        pdf.output('load.pdf')