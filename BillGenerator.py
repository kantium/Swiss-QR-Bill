#!/usr/bin/python3

import cairo
import math
import json

import qrcode
import argparse

from datetime import date, timedelta

def set_background(cr, page_width, page_height, background_path):

    image_surface = cairo.ImageSurface.create_from_png(background_path)
    #cr.set_source_surface(canvas, 0, 0)
    #cr.paint()

    img_height = image_surface.get_height()
    img_width = image_surface.get_width()
    width_ratio = float(page_width) / float(img_width)
    height_ratio = float(page_height) / float(img_height)
    scale_xy = min(height_ratio, width_ratio)
    # scale image and add it
    cr.save()
    cr.scale(scale_xy, scale_xy)
    cr.translate(0, 0)
    cr.set_source_surface(image_surface, 0, 0)

    cr.paint()
    cr.restore()


def print_qrcode(cr, qr_value, x, y):

    qr_size = 130
    cross_pos = 55
    cross_size = 20

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=10,
        border=0,
    )
    qr.add_data(qr_value)
    qr.make(fit=True)

    img = qr.make_image() #fill_color="black", back_color="yellow")
    
    img = img.convert("RGB")
    if 'A' not in img.getbands():
        img.putalpha(int(256))
    #print(img.getbands())
    #print(img.size)
    #print(type(img))
    
    arr = bytearray(img.tobytes('raw', 'BGRa'))
    surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_ARGB32, img.width, img.height)
    
    img_height = surface.get_height()
    img_width = surface.get_width()
    width_ratio = float(qr_size) / float(img_width)
    height_ratio = float(qr_size) / float(img_height)
    scale_xy = min(height_ratio, width_ratio)

    cr.save()
    cr.translate(x, y)
    
    cr.scale(scale_xy, scale_xy)
    cr.set_source_surface(surface)

    ## Print QR Code
    cr.paint()
    cr.restore()

    ## Print Swiss Cross
    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(cross_pos+x, cross_pos+y, cross_size, cross_size)
    cr.fill()

    cr.set_source_rgb(0, 0, 0)
    cr.rectangle(cross_pos+x+1.5, cross_pos+y+1.5, 17, 17)
    cr.fill()

    cr.set_source_rgb(1, 1, 1)
    cr.rectangle(cross_pos+x+4.5, cross_pos+y+8.5, 11, 3.3)
    cr.fill()
    cr.rectangle(cross_pos+x+8.5, cross_pos+y+4.5, 3.3, 11)
    cr.fill()


def print_headers(cr): 

    cr.set_font_size(30)
    cr.move_to(60, 50)
    cr.show_text(invoice_data["invoice"]["information"])

    cr.set_source_rgb(0.1, 0.1, 0.1)
    cr.set_font_size(11)

    cr.move_to(60, 80)
    cr.show_text(creditor_data["l1"])
    cr.move_to(60, 95)
    cr.show_text(creditor_data["l2"])
    cr.move_to(60, 110)
    cr.show_text(creditor_data["l3"])
    cr.move_to(60, 125)
    cr.show_text(creditor_data["l4"])
    cr.move_to(60, 140)
    cr.show_text(creditor_data["email"])
    cr.move_to(60, 155)
    cr.show_text(creditor_data["tel"])

    cr.move_to(370, 35)
    cr.show_text(language_data["clientid"])
    cr.move_to(370, 50)
    cr.show_text(language_data["invoiceid"])
    cr.move_to(370, 65)
    cr.show_text(language_data["invoicedate"])
    cr.move_to(370, 80)
    cr.show_text(language_data["duedate"])
    cr.move_to(370, 95)
    cr.show_text(language_data["totalamount"])
    
    cr.move_to(480, 35)
    cr.show_text(debtor_data["clientid"])
    cr.move_to(480, 50)
    cr.show_text(invoice_data["invoice"]["invoiceid"])
    cr.move_to(480, 65)
    cr.show_text(invoice_data["todaytxt"])
    cr.move_to(480, 80)
    cr.show_text(invoice_data["duedatetxt"])
    cr.move_to(480, 95)
    cr.show_text(invoice_data["totalamounttxt"] + " " + invoice_data["invoice"]["currency"])

    cr.move_to(310, 170)
    cr.show_text(debtor_data["l1"])
    cr.move_to(310, 185)
    cr.show_text(debtor_data["l2"])
    cr.move_to(310, 200)
    cr.show_text(debtor_data["l3"])
    cr.move_to(310, 215)
    cr.show_text(debtor_data["l4"])


def print_company_logo(cr, logo_path):

    image_surface = cairo.ImageSurface.create_from_png(logo_path)
    cr.set_source_surface(image_surface, 20, 20)
    cr.paint()

    cr.select_font_face("Sans", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_BOLD)
    cr.set_source_rgb(0, 0, 0)

    cr.set_font_size(30)
    cr.move_to(120, 50)
    cr.show_text(creditor_data["company"])


def print_table(cr):

    cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_source_rgb(0.3, 0.3, 0.3)

    cr.set_font_size(10)
    cr.move_to(40, 270)
    cr.show_text(language_data["items"])
    cr.move_to(330, 270)
    cr.show_text(language_data["amount"])
    cr.move_to(390, 270)
    cr.show_text(language_data["price"])
    cr.move_to(470, 270)
    cr.show_text(language_data["total"] + " (" + invoice_data["invoice"]["currency"] + ")")

    cr.set_line_width(0.5)
    cr.move_to(40, 277)
    cr.line_to(555, 277) 
    cr.stroke()

    for index, item in enumerate(invoice_data["items"], start=1):
        cr.set_source_rgb(0.1, 0.1, 0.1)
        cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        cr.set_font_size(12)
        cr.move_to(40, 270+index*25)
        cr.show_text("{0}".format(item["name"]))

        cr.set_source_rgb(0.3, 0.3, 0.3)
        cr.set_font_size(10)
        cr.move_to(330, 270+index*25)
        cr.show_text("{: .2f}".format(item["amount"]))
        cr.move_to(390, 270+index*25)
        cr.show_text("{0:,.2f}".format(item["price"]).replace(","," "))

        cr.set_source_rgb(0.1, 0.1, 0.1)
        cr.set_font_size(12)
        cr.move_to(470, 270+index*25)
        cr.show_text("{0:,.2f}".format(item["amount"]*item["price"]).replace(","," "))

    cr.set_line_width(0.5)
    cr.move_to(40, 282+(len(invoice_data["items"]))*25)
    cr.line_to(555, 282+(len(invoice_data["items"]))*25) 
    cr.stroke()

    cr.set_source_rgb(0.1, 0.1, 0.1)
    cr.set_font_size(12)
    cr.move_to(40, 277+(len(invoice_data["items"])+1)*25)
    cr.show_text(language_data["subtotal"])
    cr.set_source_rgb(0.1, 0.1, 0.1)
    cr.move_to(470, 277+(len(invoice_data["items"])+1)*25)
    cr.show_text(invoice_data["totalamounttxt"])


def print_receipt(cr, page_width, page_height, debug_mode):

    if debug_mode:
        cr.set_source_rgb(1, 0.2, 0.2)
    else:
        cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(0.5)
    cr.move_to(0, 544)
    cr.line_to(page_width, 544) 
    cr.stroke()

    cr.set_line_width(0.5)
    cr.move_to(175.5, 544)
    cr.line_to(175.5, page_height) 
    cr.stroke()

    cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    if debug_mode:
        cr.set_source_rgb(0.2, 0.9, 0.1)
    cr.set_font_size(20)
    cr.move_to(13, 551)
    cr.show_text("✂")

    # Rotated Scissor
    rotation = 90 * math.pi / 180
    cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    if debug_mode:
        cr.set_source_rgb(0.4, 0.4, 0.9)
    cr.set_font_size(20)
    fascent, fdescent, fheight, fxadvance, fyadvance = cr.font_extents()
    cr.save()
    cr.translate(180,565)
    cr.rotate(rotation)
    xoff, yoff, textWidth, textHeight = cr.text_extents("✂")[:4]
    offx = -textWidth / 2.0
    offy = (fheight / 2.0)
    cr.move_to(offx, offy)
    cr.show_text("✂")
    cr.restore()

    cr.select_font_face("Arimo", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    if debug_mode:
        cr.set_source_rgb(0.7, 0.3, 0.7)
    
    cr.set_font_size(8)
    cr.move_to(14, 592)
    cr.show_text(creditor_data["iban"])
    cr.move_to(14, 601)
    cr.show_text(creditor_data["l1"])
    cr.move_to(14, 610)
    cr.show_text(creditor_data["l2"])
    cr.move_to(14, 619)
    cr.show_text(creditor_data["l3"])
    cr.move_to(14, 628)
    cr.show_text(creditor_data["l4"])

    cr.set_font_size(8)
    cr.move_to(14, 675)
    cr.show_text(debtor_data["l1"])
    cr.move_to(14, 684)
    cr.show_text(debtor_data["l2"])
    cr.move_to(14, 693)
    cr.show_text(debtor_data["l3"])
    cr.move_to(14, 702)
    cr.show_text(debtor_data["l4"])

    cr.set_font_size(8)
    cr.move_to(14, 752)
    cr.show_text(invoice_data["invoice"]["currency"])
    cr.move_to(48, 752)
    cr.show_text(invoice_data["totalamounttxt"])

    cr.set_font_size(10)
    cr.move_to(334, 575)
    cr.show_text(creditor_data["iban"])
    cr.move_to(334, 586)
    cr.show_text(creditor_data["l1"])
    cr.move_to(334, 597)
    cr.show_text(creditor_data["l2"])
    cr.move_to(334, 608)
    cr.show_text(creditor_data["l3"])
    cr.move_to(334, 619)
    cr.show_text(creditor_data["l4"])

    if not invoice_data["invoice"]["reference"] == "":
        cr.set_font_size(10)
        cr.move_to(334, 643)
        cr.show_text(invoice_data["invoice"]["reference"])

        cr.set_font_size(8)
        cr.move_to(14, 647)
        cr.show_text(invoice_data["invoice"]["reference"])
        cr.move_to(334, 632)
        cr.show_text(language_data["reference"])

        cr.set_font_size(6)
        cr.move_to(14, 638)
        cr.show_text(language_data["reference"])

    cr.set_font_size(10)
    cr.move_to(334, 677)
    cr.show_text(invoice_data["invoice"]["information"])
    cr.move_to(334, 732)
    cr.show_text(debtor_data["l1"])
    cr.move_to(334, 743)
    cr.show_text(debtor_data["l2"])
    cr.move_to(334, 754)
    cr.show_text(debtor_data["l3"])
    cr.move_to(334, 765)
    cr.show_text(debtor_data["l4"])
    cr.move_to(189.5, 756)
    cr.show_text(invoice_data["invoice"]["currency"])
    cr.move_to(229, 756)
    cr.show_text(invoice_data["totalamounttxt"])

    cr.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    if debug_mode:
        cr.set_source_rgb(0.3, 0.7, 0.7)

    cr.set_font_size(11)
    cr.move_to(14, 567)
    cr.show_text(language_data["receipt"])
    cr.move_to(189.5, 567)
    cr.show_text(language_data["paymentpart"])

    cr.set_font_size(6)
    cr.move_to(14, 583)
    cr.show_text(language_data["payableto"])
    cr.move_to(14, 666)
    cr.show_text(language_data["payableby"])
    cr.move_to(14, 742)
    cr.show_text(language_data["currency"])
    cr.move_to(48, 742)
    cr.show_text(language_data["amount"])
    cr.move_to(112, 781)
    cr.show_text(language_data["acceptance"])

    cr.set_font_size(8)
    cr.move_to(334, 565)
    cr.show_text(language_data["payableto"])
    cr.move_to(334, 666)
    cr.show_text(language_data["additionalinformation"])
    cr.move_to(334, 722)
    cr.show_text(language_data["payableby"])
    cr.move_to(189.5, 743)
    cr.show_text(language_data["currency"])
    cr.move_to(229, 743)
    cr.show_text(language_data["amount"])

# In debug mode, print C5 Envelop lines
def print_paper_cut(cr, page_width, page_height):
    cr.set_source_rgb(0.7, 1, 0.7)
    cr.set_line_width(0.5)
    cr.move_to(0, page_height/2)
    cr.line_to(page_width, page_height/2) 
    cr.stroke()

    cr.move_to(0, page_height/3*2)
    cr.line_to(page_width, page_height/3*2) 
    cr.stroke()

    cr.move_to(0, page_height/3)
    cr.line_to(page_width, page_height/3) 
    cr.stroke()

    cr.move_to(257, 135)
    cr.line_to(257, 239) 
    cr.stroke()
    cr.move_to(257, 135)
    cr.line_to(543, 135) 
    cr.stroke()
    cr.move_to(257, 239)
    cr.line_to(543, 239) 
    cr.stroke()
    cr.move_to(543, 135)
    cr.line_to(543, 239) 
    cr.stroke()

# QR Data Generation 
def gen_qr_data():
    spc = [None] * 31
    spc[0] = "SPC"
    spc[1] = "0200"
    spc[2] = "1"
    spc[3] = creditor_data["iban"].replace(" ", "")
    spc[4] = "K" # K = Adresse sur deux lignes, S = Addresse structurée (4 lignes voir doc)
    spc[5] = creditor_data["name"]
    spc[6] = creditor_data["address1"]
    spc[7] = creditor_data["address2"]
    spc[8] = ""
    spc[9] = ""
    spc[10] = "CH"
    spc[11] = ""
    spc[12] = ""
    spc[13] = ""
    spc[14] = ""
    spc[15] = ""
    spc[16] = ""
    spc[17] = ""
    spc[18] = str(invoice_data["totalamount"])
    spc[19] = invoice_data["invoice"]["currency"]
    spc[20] = "K"
    spc[21] = debtor_data["name"]
    spc[22] = debtor_data["address1"]
    spc[23] = debtor_data["address2"]
    spc[24] = ""
    spc[25] = ""
    spc[26] = "CH"
    spc[27] = invoice_data["invoice"]["ref_type"] 
    spc[28] = invoice_data["invoice"]["reference"].replace(" ", "")
    spc[29] = invoice_data["invoice"]["information"]
    spc[30] = "EPD"

    return "\n".join(spc)


def main(debug_mode):

    # A4 size in Pixel
    page_width = 595
    page_height = 842
    background_path = "./PaymentPartReceipt_A4_en_LIBERATION_SANS.png"
    logo_path = "./logo408.png"
    output_path = invoice_data["invoice"]["invoiceid"].strip().replace(" ","_") + ".pdf"
    qrcode_pos_x = 189.5
    qrcode_pos_y = 592.5
    
    invoice_data["totalamount"] = round(sum([x["amount"]*x["price"] for x in invoice_data["items"]]),2)
    invoice_data["totalamounttxt"] = "{:,.2f}".format(invoice_data["totalamount"]).replace(","," ")
    assert(invoice_data["totalamount"] > 0)

    if debug_mode:
        invoice_data["totalamount"] = 0.00
        invoice_data["totalamounttxt"] = "0.00"
        invoice_data["invoice"]["information"] = language_data["dummy"]
    
    if invoice_data["invoice"]["reference"].strip() != "":
        invoice_data["invoice"]["reference"] = invoice_data["invoice"]["reference"].strip()
        invoice_data["invoice"]["ref_type"] = "QRR"
        assert(len(invoice_data["invoice"]["reference"].replace(" ", "")) == 27)
    else:
        invoice_data["invoice"]["ref_type"] = "NON"
        invoice_data["invoice"]["reference"] = ""

    invoice_data["today"] = date.today()
    invoice_data["todaytxt"] = date.strftime(invoice_data["today"], "%d.%m.%y")
    invoice_data["duedate"] = date.today() + timedelta(days=invoice_data["invoice"]["duedays"])
    invoice_data["duedatetxt"] = date.strftime(invoice_data["duedate"], "%d.%m.%y")
    
    assert(len(invoice_data["invoice"]["information"]) < 140)
    assert(invoice_data["invoice"]["currency"] == "CHF" or invoice_data["invoice"]["currency"] == "EUR")
    
    assert(len(debtor_data["address1"]) <= 70)
    assert(len(debtor_data["address2"]) <= 70)
    assert(len(creditor_data["address1"]) <= 70)
    assert(len(creditor_data["address1"]) <= 70)

    ps = cairo.PDFSurface(output_path, page_width, page_height)
    cr = cairo.Context(ps)

    if debug_mode:
        set_background(cr, page_width, page_height, background_path)
        print_paper_cut(cr, page_width, page_height)

    print_table(cr)
    print_headers(cr)

    if debug_mode:
        qrcode_data = "A"*800
    else:
        qrcode_data = gen_qr_data()
    print_qrcode(cr, qrcode_data, qrcode_pos_x, qrcode_pos_y)

    #print_company_logo(cr, logo_path)

    print_receipt(cr, page_width, page_height, debug_mode)
    
    cr.show_page()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='QRBill Invoice Generator')
    parser.add_argument('-c','--creditor', help='Person who receive money', required=True)
    parser.add_argument('-d','--debtor', help='Billed person', required=True)
    parser.add_argument('-i','--invoice', help='Invoice content', required=True)
    parser.add_argument('-l','--language',
                    default='en',
                    const='en',
                    nargs='?',
                    choices=['en', 'fr', 'de', 'it'],
                    help='list of language (default: %(default)s)')
    parser.add_argument('--debug', action='store_true')

    args = vars(parser.parse_args())

    with open(args["creditor"]) as json_creditor:
        creditor_data = json.load(json_creditor)
    
    with open(args["invoice"]) as json_invoice:
        invoice_data = json.load(json_invoice)
    
    with open(args["debtor"]) as json_debtor:
        debtor_data = json.load(json_debtor)
    
    with open("Languages/" + args["language"]+".json") as json_language:
        language_data = json.load(json_language)
    
    if len(debtor_data["name"]) >= 30:
        x = debtor_data["name"][30:].split(" ",1)
        debtor_data["l1"] = debtor_data["name"][:30]+x[0]
        debtor_data["l2"] = x[1]
        debtor_data["l3"] = debtor_data["address1"]
        debtor_data["l4"] = debtor_data["address2"]
    else:
        debtor_data["l1"] = debtor_data["name"]
        debtor_data["l2"] = debtor_data["address1"]
        debtor_data["l3"] = debtor_data["address2"]
        debtor_data["l4"] = ""

    if len(creditor_data["name"]) >= 30:
        x = creditor_data["name"][30:].split(" ",1)
        creditor_data["l1"] = creditor_data["name"][:30]+x[0]
        creditor_data["l2"] = x[1]
        creditor_data["l3"] = creditor_data["address1"]
        creditor_data["l4"] = creditor_data["address2"]
    else:
        creditor_data["l1"] = creditor_data["name"]
        creditor_data["l2"] = creditor_data["address1"]
        creditor_data["l3"] = creditor_data["address2"]
        creditor_data["l4"] = ""

    main(args["debug"])

