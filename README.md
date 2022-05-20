# Python Swiss QR-Bill Generator

## Introduction

Easy usable Python script to generate QR-Bill following the SIX implementation guidlines. QR-Bill is also known as QR-Rechnung in the German part and QR-Facture for the Romands.

Deptor name and address fit in a C5 envelope with right side window

## Requirements

- python (3.4+)
- pip

## Installation

```bash
git clone https://github.com/kantium/Swiss-QR-Bill.git
cd Swiss-QR-Bill
pip install -r requirements.txt
```

## Updating

```bash
git fetch
```

## Configuring

Three JSON files need to be customized for your needs, these files are located in the `Creditors`, `Debtors` and `Invoices` folders. 


## Usage

```bash
./BillGenerator.py -c Creditors/Robert.json -d Debtors/Maria.json -i Invoices/Invoice_220506_522.json -l fr
```

## Features

- [x] Invoice
- [x] Languages (FR/EN)
- [x] QR-Bill without reference number
- [ ] QR-IBAN and QR

## Documentation

PDF files like the SIX Implementation Guide can be found in the Documentation folder

```bash
./BillGenerator.py -h
usage: BillGenerator.py [-h] -c CREDITOR -d DEBTOR -i INVOICE
                        [-l [{en,fr,de,it}]] [--debug]

QRBill Invoice Generator

options:
  -h, --help            show this help message and exit
  -c CREDITOR, --creditor CREDITOR
                        Person who receive money
  -d DEBTOR, --debtor DEBTOR
                        Billed person
  -i INVOICE, --invoice INVOICE
                        Invoice content
  -l [{en,fr,de,it}], --language [{en,fr,de,it}]
                        list of language (default: en)
  --debug
```

## Contributing

You are welcome to help by openning an issue or proposing changes

