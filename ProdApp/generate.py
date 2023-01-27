# Importing Required Module
import os

from reportlab.pdfgen import canvas
import os
from PIL import (Image,
                 ImageFont,
                 ImageDraw)

def generate_invoice(pattern):

    products_length = len(pattern['products'])
    all_length = products_length * 10

    # Creating Canvas
    return_id = str(pattern['id']).replace('#', '')
    c = canvas.Canvas("images/invoices/invoice"+ return_id + ".pdf",pagesize=(200,250+ all_length),bottomup=0)

    # Logo Section
    # Setting th origin to (10,40)
    c.translate(10,40)
    # Inverting the scale for getting mirror Image of logo
    c.scale(1,-1)
    # Inserting Logo into the Canvas at required position
    c.drawImage("images/gtilogo.png",0,0,width=50,height=30)

    # Title Section
    # Again Inverting Scale For strings insertion
    c.scale(1,-1)
    # Again Setting the origin back to (0,0) of top-left
    c.translate(-10,-40)
    # Setting the font for Name title of company
    c.setFont("Helvetica-Bold",10)
    # Inserting the name of the company
    c.drawCentredString(125,20,"Green Tech Innovation")
    # For under lining the title
    c.line(70,22,180,22)
    # Changing the font size for Specifying Address
    c.setFont("Helvetica-Bold",5)
    c.drawCentredString(125,30,"Block No. 101, Triveni Apartments, Pitam Pura,")
    c.drawCentredString(125,35,"New Delhi - 110034, India")
    # Changing the font size for Specifying GST Number of firm
    c.setFont("Helvetica-Bold",6)
    c.drawCentredString(125,42,"IFU : 07AABCS1429B1Z")

    # Line Seprating the page header from the body
    c.line(5,45,195,45)

    # Document Information
    # Changing the font for Document title
    c.setFont("Courier-Bold",8)
    c.drawCentredString(100,55,"FACTURE DE COMMANDE")
    c.drawCentredString(100, 60, str(pattern['ship_option'] + ': {}'.format(pattern['ship_price'])))

    # This Block Consist of Costumer Details
    c.roundRect(15,63,170,40,10,stroke=1,fill=0)
    c.setFont("Times-Bold",5)
    c.drawRightString(60,70,"FACTURE No. :")
    c.drawRightString(60,80,"DATE :")
    c.drawRightString(60,90,"ACHETEUR :")
    c.drawRightString(60,100,"PHONE No. :")

    c.drawRightString(80, 70, str(pattern['id']))
    c.drawRightString(90, 80, str(pattern['date']))
    c.drawRightString(110, 90, str(pattern['user']['first_name']) + " " + str(pattern['user']['last_name']))
    c.drawRightString(80, 100, str(pattern['user']['contact']))

    c.drawRightString(130,70,"LIVRAISON:")
    c.drawRightString(130,80,"ADDRESSE  :")
    c.drawRightString(130,90,"VILLE :")
    c.drawRightString(130,100,"PHONE No :")

    c.drawRightString(175, 70, str(pattern['livraison']['first_name']) + " " + str(pattern['livraison']['last_name']))
    c.drawRightString(175, 80, str(pattern['livraison']['address']))
    c.drawRightString(175, 90, str(pattern['livraison']['city']))
    c.drawRightString(175, 100,str(pattern['livraison']['phone_number']))

    #Addresse Livraison




    # This Block Consist of Item Description
    c.roundRect(15,108,170,130+ all_length,10,stroke=1,fill=0)
    c.line(15,120,185,120)
    c.drawCentredString(25,118,"SR No.")
    c.drawCentredString(75,118,"GOODS DESCRIPTION")
    c.drawCentredString(125,118,"RATE")
    c.drawCentredString(148,118,"QTY")
    c.drawCentredString(173,118,"TOTAL")
    # Drawing table for Item Description
    i=0
    
    for product in pattern['products']:
        c.drawCentredString(25,130 + i,str(product['id']))
        c.drawCentredString(75,130 + i ,str(product['name']))
        c.drawCentredString(125,130 + i, str(product['price']))
        c.drawCentredString(148,130 + i,str(product['quantity']))
        c.drawCentredString(173,130 + i,str(product['total']))
        i = i + 10
    

    
    

    c.line(15,210+ all_length,185,210+ all_length)
    c.line(35,108,35,220+ all_length) 
    c.line(115,108,115,220+ all_length)
    c.line(135,108,135,220+ all_length)
    c.line(160,108,160,220+ all_length)

    # Declaration and Signature
    total = pattern['all_total']
    c.line(15,220+ all_length,185,220+ all_length)
    c.drawCentredString(25,215+ all_length,"")
    c.drawCentredString(75,215+ all_length,"")
    c.drawCentredString(125,215 + all_length,"")
    c.drawCentredString(148,215+ all_length,"")
    c.drawCentredString(173,215+ all_length,str(total))
    c.line(100,220+ all_length,100,238+ all_length)
    c.drawString(20,225+ all_length,"We declare that above mentioned")
    c.drawString(20,230+ all_length,"information is true.")
    c.drawString(20,235+ all_length,"(This is system generated invoive)")
    c.drawImage(pattern['file_qrcode'], 160, 250, width=20, height=20)


    # End the Page and Start with new
    c.showPage()
    # Saving the PDF
    c.save()

    return open("images/invoices/invoice"+ return_id + ".pdf", mode='rb')

data_invoice = {'id': 'cpm1',
            'livraison':{'first_name': 'john','last_name':'oke','address':'12 street','phone_number':'123443','city':'Cotonou'},
            'user': {'first_name': 'john','last_name':'oke','contact':'124432'},
            'products':[{'id':'prod1','name':'produit','price':123,'quantity': 3, 'total': 4}],
            'all_total': 137,
            'date': 'March',
            }

#print(type(generate_invoice(data_invoice)))

def add_logo_to_img(file_path):

    LOGO_FILENAME = 'images/logo.png'
    logoIm = Image.open(LOGO_FILENAME).convert("RGBA")
    default_font_size = 10
    # text = ''
    # text_width, text_height = ImageFont.truetype(r'C:\Windows\Fonts\IMPACT.TTF').getsize(text)
    file = Image.open(file_path)
    width, height = file.size

    font = ImageFont.truetype('images/IMPACT.TTF', 15)

    sLogo = logoIm.resize((int(width / 9), int(height / 9)))
    sLogoWidth, sLogoHeight = sLogo.size

    # Add the logo.
    for i in range(sLogoHeight, sLogoHeight + 200, sLogoHeight):
        file.paste(sLogo, (width - i, height - sLogoHeight), sLogo)

    draw = ImageDraw.Draw(file)
    draw.text((10, 10), 'Green Tech Innovation ©', font=font, fill=(128, 128, 128))

    file.save(file_path)



