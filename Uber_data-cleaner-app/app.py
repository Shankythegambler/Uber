from flask import Flask, request, send_file
import pandas as pd
import re

app = Flask(__name__)

# ---------------- FUNCTIONS ----------------
def clean_text_proper(text):
    if pd.isna(text) or str(text).strip() == "":
        return ""
    cleaned = re.sub(r'[-+%,]', '', str(text)).strip()
    return cleaned.title()

def split_name(name):
    parts = str(name).split()
    if len(parts) == 1:
        return parts[0], "", ""
    if len(parts) == 2:
        return parts[0], "", parts[1]
    return parts[0], " ".join(parts[1:-1]), parts[-1]

def format_dob(val):
    try:
        if pd.isna(val) or str(val).strip() == "":
            return ""
        return pd.to_datetime(val).strftime('%Y-%m-%d')
    except:
        return str(val)

# ---------------- ROUTE: HOME ----------------
@app.route('/')
def home():
    return open("index.html").read()

# ---------------- ROUTE: UPLOAD ----------------
@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    df = pd.read_csv(file, encoding="latin1")

    # 🔥 CLEANING LOGIC START
    df['Candidate Name'] = df.iloc[:, 1].apply(clean_text_proper)

    df[['First', 'Middle', 'Last']] = df['Candidate Name'].apply(
        lambda x: pd.Series(split_name(x))
    )

    # 🔥 FINAL OUTPUT
    final = pd.DataFrame()

    final['A_First_Name'] = df['First']
    final['B_Middle_Name'] = df['Middle']
    final['C_Last_Name'] = df['Last']
    final['D_Father_Name'] = df.iloc[:, 2]
    final['E_Mobile'] = ""
    final['F_DOB'] = df.iloc[:, 3].apply(format_dob)
    final['G_Location'] = "496380"
    final['H_Case_Insuff'] = ""
    final['I_Case_Comment'] = ""
    final['J_Car_No'] = "NOT MENTIONED"
    final['K'] = "NOT MENTIONED"
    final['L'] = "NOT MENTIONED"
    final['M_UUID'] = df.iloc[:, 0]
    final['N_Special_ID'] = ""
    final['O_Mode'] = "OFFLINE"
    final['P_Permanent_Insuff'] = ""
    final['Q_Name'] = df['Candidate Name']
    final['R_Type'] = ""
    final['S_Address'] = df.iloc[:, 4]
    final['T_Pin'] = ""
    final['U_Insuff'] = ""
    final['V_City'] = ""
    final['W_Priority'] = ""

    # 🔥 SAVE FILE
    output_file = "output.csv"
    final.to_csv(output_file, index=False)

    return send_file(output_file, as_attachment=True)

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)