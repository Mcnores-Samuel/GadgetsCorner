#!/usr/bin/env python3
import PyPDF2
import re
from write_to_json import save_to_json_file, load_from_json_file


def read_pdf_to_text(filename):
    """Extracts Text format data from pdf file.

    args:
        filename: The name of the file or file pathname.
    Returns: Newline separated string from the pdf file.
    """
    try:
        with open(filename, "rb") as file:
            data = PyPDF2.PdfReader(file)
            pages = len(data.pages)
            string = ""
            for page_num in range(pages):
                page = data.pages[page_num]
                string += page.extract_text()
        return (string)
    except (FileExistsError, FileNotFoundError) as err:
        print(err)
        return ""


def extract_contract_number(text):
    """Extracts text matching the regular expression from the text

    args:
        text: The text to look for the specific patterns.
    Return: text matching the patterns.
    """
    regex = r"[A-Z]{1}\d{8}"
    matches = re.findall(regex, text)
    # try:
    #     data_list = load_from_json_file("contracts.json")
    # except FileNotFoundError:
    #     data_list = []
    # data = matches[:]
    # data_list += data
    # save_to_json_file(data_list, "contracts.json")
    return (matches)


if __name__ == "__main__":
    text_data = read_pdf_to_text("generated (2).pdf")
    bank_paymets = extract_contract_number(text_data)
    print("Contracts numbers from bank statement: ",len(bank_paymets))
    data = read_pdf_to_text("Merchant Contract Payments (4).pdf")
    contracts_data = extract_contract_number(data)
    print("Contracts numbers from Merchant Customers: ",len(contracts_data))
    not_found = []
    for contract in contracts_data:
        if contract in bank_paymets:
            print("Bank Payment Contract: {}  matches with Merchant Customers Contract: {}".format(bank_paymets[bank_paymets.index(contract)], contract))
        else:
            not_found.append(contract)
    print()
    print("Contracts not found in bank payments: ", len(not_found))
    for contract in not_found:
        print("Contract not found in bank Statement: ", contract)