from fastapi import APIRouter
from xml.etree import ElementTree as ET
import pandas as pd
from fastapi.responses import FileResponse
import os
import time

convertor_router = APIRouter()

@convertor_router.post("/convert/{file_path:path}")
def convert(file_path : str):

    tree = ET.parse(file_path)
    root = tree.getroot()
    print(root.tag)

    transactions = []
    for voucher in root.findall(".//VOUCHER"):
        if voucher.get("VCHTYPE") == "Receipt":
            transaction = {
                "Date": voucher.findtext("DATE") if voucher.findtext("DATE") else "NA",
            "Transaction_type": voucher.findtext(".//ALLLEDGERENTRIES.LIST//BANKALLOCATIONS.LIST//TRANSACTIONTYPE") if voucher.findtext(".//ALLLEDGERENTRIES.LIST//BANKALLOCATIONS.LIST//TRANSACTIONTYPE") else "NA",
            "Vch No": voucher.findtext("VOUCHERNUMBER") if voucher.findtext("VOUCHERNUMBER") else "NA",
            "Ref No": voucher.findtext(".//ALLLEDGERENTRIES.LIST//BANKALLOCATIONS.LIST//UNIQUEREFERENCENUMBER") if voucher.findtext(".//ALLLEDGERENTRIES.LIST//BANKALLOCATIONS.LIST//UNIQUEREFERENCENUMBER") else "NA",
            "Ref Type": voucher.findtext(".//ALLLEDGERENTRIES.LIST//BANKALLOCATIONS.LIST//BILLTYPE") if voucher.findtext(".//ALLLEDGERENTRIES.LIST//BANKALLOCATIONS.LIST//BILLTYPE") else "NA",
            "Ref Date" : voucher.findtext("REFERENCEDATE") if voucher.findtext("REFERENCEDATE") else "NA",
            "Debtor" : voucher.findtext("PARTYNAME") if voucher.findtext("PARTYNAME") else "NA",
            "Amount": voucher.findtext(".//ALLLEDGERENTRIES.LIST//AMOUNT") if voucher.findtext(".//ALLLEDGERENTRIES.LIST//AMOUNT") else "NA",
            "Particulars" : voucher.findtext("PARTYLEDGERNAME") if voucher.findtext("PARTYLEDGERNAME") else "NA",
            "Vch_type" : voucher.findtext("VOUCHERTYPENAME") if voucher.findtext("VOUCHERTYPENAME") else "NA",

            }
            transactions.append(transaction)
    

    df = pd.DataFrame(transactions)
    df["Date"] = pd.to_datetime(df["Date"], format="%Y%m%d").dt.date

    file_id = file_path.split("\\")[1]
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    unique_file_id = f"{file_id}_{timestamp}"
    save_path = os.path.join("output_file", unique_file_id)
    os.makedirs(save_path, exist_ok=True)

    file_path = os.path.join(save_path, "result.xlsx")
    # output_path = f"output_file\{file_id}\result.xlsx"

    df.to_excel(file_path, index=False)

    return FileResponse(
        path=file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="result.xlsx"
    )


    