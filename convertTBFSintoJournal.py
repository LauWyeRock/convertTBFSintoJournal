import pandas as pd
from openpyxl import load_workbook
import streamlit as st
from functools import reduce

def process_file(file, sheet_name, skip_rows, last_row_to_skip, column_names):
    wb = load_workbook(file, data_only=True)
    ws = wb[sheet_name]

    data = pd.DataFrame(ws.values)
    
    if column_names:
        data.columns = column_names
    else:
        header_row = data.iloc[skip_rows]
        header_row[0] = 'Account'  
        data.columns = header_row
    
    data = data.iloc[skip_rows + 1:]  
    if last_row_to_skip:
        data = data[:-last_row_to_skip]

    data.reset_index(drop=True, inplace=True)

    for col in data.columns[1:]:  
        data[col] = pd.to_numeric(data[col], errors='coerce')
    data.fillna(0, inplace=True)

    return data

def main():
    st.title("Financial Data Processor")

    tb_file = st.file_uploader("Upload Trial Balance", type=['xlsx'])
    bs_file = st.file_uploader("Upload Balance Sheet", type=['xlsx'])
    pl_file = st.file_uploader("Upload Profit & Loss", type=['xlsx'])

    if st.button("Process Files"):
        if tb_file and bs_file and pl_file:
            tb_data = process_file(tb_file, 'Trial Balance', 4, 1, ['Account', 'TB Debit', 'TB Credit'])
            bs_data = process_file(bs_file, 'Balance Sheet', 4, 1, ['Account', 'BS Amount'])
            pl_data = process_file(pl_file, 'Profit and Loss', 4, 1, ['Account', 'P&L Amount'])

            
            dfs = [tb_data.set_index('Account'), bs_data.set_index('Account'), pl_data.set_index('Account')]
            combined_data = reduce(lambda left, right: pd.merge(left, right, on='Account', how='outer'), dfs).fillna(0).reset_index()

            output_df = pd.DataFrame({
                'Journal Reference': 'FYE2023 Conversion: Transfer Balance',
                'Contact': None,
                'Date': None,
                'Account': combined_data['Account'],
                'Description': None,
                'Tax Included in Amount': None,
                'Debit Amount': combined_data['TB Debit'],
                'Credit Amount': combined_data['TB Credit'],
                'TB Debit': combined_data['TB Debit'],
                'TB Credit': combined_data['TB Credit'],
                'BS Amount': combined_data['BS Amount'],
                'P&L Amount': combined_data['P&L Amount']
            })

            csv = output_df.to_csv(index=False)
            st.download_button("Download CSV", csv, "financial_data.csv", "text/csv", key='download-csv')
        else:
            st.error("Please upload all files to process.")

if __name__ == "__main__":
    main()
