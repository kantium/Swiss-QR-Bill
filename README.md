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

Creditor and debtor addresses are structured (address type `S`, required by the Swiss QR Code since Implementation Guidelines v2.3). Use the fields `street`, `house_number`, `postal_code`, `town` and `country` (optional, 2-letter ISO 3166-1 code such as `CH` or `LI`, defaults to `CH`).

```json
"street":       "Rue du Lac",
"house_number": "1268",
"postal_code":  "2501",
"town":         "Biel",
"country":      "CH"
```

- `postal_code` and `town` are mandatory, `street` and `house_number` can be left empty (`""`).
- `postal_code` is the number only (`2501`, not `CH-2501`).
- `country` is converted to uppercase and must be exactly two letters (`Switzerland` is rejected).

The invoice `information` (unstructured message) is limited to 140 characters.


## Usage

```bash
./BillGenerator.py -c Creditors/Robert.json -d Debtors/Maria.json -i Invoices/Invoice_220506_522.json -l fr
```

## Features

- [x] PDF Invoice generation
- [x] Languages (FR/EN)
- [x] Without Reference number (NON)
- [x] With Reference number (QRR)
- [x] Structured Address
- [ ] IBAN and Reference number checksum
- [ ] German translation
- [ ] ISO Country Code check

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

Thanks to [Tiralka](https://github.com/Tiralka) for switching the Swiss QR Code to structured addresses (type `S`), required since the SIX Implementation Guidelines v2.3.

