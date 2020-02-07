#!/bin/env pytho/bin/env python -m pip install --upgrade mymodulen
import urllib
import re
import numpy as np
from pandas import DataFrame
from bs4 import BeautifulSoup
import PyPDF2
import pdb



#2015 to 2019


def download_and_parse_letter(letter_url):
    file_path = 'approval_letter_%s' % letter_url
    try: 
        urllib.urlretrieve(letter_url, 'file')
        object = PyPDF2.PdfFileReader('file')
        NumPages = object.getNumPages()
        String = 'postmarketing'
        match = False
        for i in range(0, NumPages):
            PageObj = object.getPage(i)
            Text = PageObj.extractText()
            ResSearch = re.search(String, Text)
            if str(ResSearch) != 'None':
                match = True
                break
    except:
        match = 'error'
    return match

def get_15_to_19_data():
    years = [2015, 2016, 2017, 2018, 2019]
    drug_names = []
    approval_letter_links = []
    post_marketing_requirements = []

# find pdfs, add to dataframe

    for year in years:
        print year
        all_drugs_for_year_url = \
            'https://www.fda.gov/drugs/new-drugs-fda-cders-new-molecular-entities-and-new-therapeutic-biological-products/novel-drug-approvals-%s' \
            % year
        page = urllib.urlopen(all_drugs_for_year_url)
        page_html = BeautifulSoup(page, 'html.parser')
        table = page_html.find('table')
        table_body = table.find('tbody')
        drug_links = table_body.find_all('a',
                href=re.compile('accessdata'))
        for individual_drug_url in drug_links:
            drug_name = individual_drug_url.string
            print drug_name
            try:
                page = urllib.urlopen(individual_drug_url['href'])
                page_html = BeautifulSoup(page, 'html.parser')
                approval_letter = page_html.find('a', text='Letter (PDF)')
                approval_letter_link = approval_letter['href']

            # download approval letter

                urllib.urlretrieve(approval_letter_link,'approval_letter')

            # look for key word

                object = PyPDF2.PdfFileReader('approval_letter')
                NumPages = object.getNumPages()
                String = 'postmarketing'
                match = False
                for i in range(0, NumPages):
                    PageObj = object.getPage(i)
                    print 'this is page ' + str(i)
                    Text = PageObj.extractText()

                    # print(Text)

                    ResSearch = re.search(String, Text)
                    print ResSearch
                    if str(ResSearch) != 'None':
                        match = True
                        break
                post_marketing_requirements.append(match)
                drug_names.append(drug_name)
                approval_letter_links.append(approval_letter_link)
                print approval_letter_link
            except:
                print 'something went wrong for %s' % drug_name
    df = DataFrame({'Drug Names': drug_names,
                   'Approval Letters': approval_letter_links,
                   'Post Marketing Requirements': post_marketing_requirements})
    df.to_excel('phasefour.xlsx', sheet_name='sheet1', index=False)

    
def get_11_to_14_data():

    url2011 = "http://wayback.archive-it.org/7993/20170111075028/http://www.fda.gov/Drugs/DevelopmentApprovalProcess/DrugInnovation/ucm285554.htm"
    url2012 = "http://wayback.archive-it.org/7993/20170111075026/http://www.fda.gov/Drugs/DevelopmentApprovalProcess/DrugInnovation/ucm336115.htm"
    url2013 = "http://wayback.archive-it.org/7993/20170111075024/http://www.fda.gov/Drugs/DevelopmentApprovalProcess/DrugInnovation/ucm381263.htm"
    url2014 = "http://wayback.archive-it.org/7993/20170111075020/http://www.fda.gov/Drugs/DevelopmentApprovalProcess/DrugInnovation/ucm429247.htm"
    urls = [url2011, url2012, url2013, url2014]
    #urls = [url2011]
    drug_names = []
    approval_letter_links = []
    post_marketing_requirements = []

    for url in urls:
        year = url
        page = urllib.urlopen(url)
        page_html = BeautifulSoup(page, 'html.parser')
        table = page_html.find('table')
        table_body = table.find('tbody')
        drug_links = table_body.find_all('a',href=re.compile('accessdata'))
        for individual_drug_url in drug_links:
            print individual_drug_url.string == ' '
            drug_name = individual_drug_url.string if individual_drug_url.string != ' ' else 'unknown'
        #strip everything before www
            index = individual_drug_url['href'].find('http://www')
            real_url = individual_drug_url['href'][index:]
            try: 
                page = urllib.urlopen(real_url)
                page_html = BeautifulSoup(page, 'html.parser')
                approval_letter = page_html.find('a', text='Letter (PDF)')
                approval_letter_link = approval_letter['href']   
                drug_names.append(drug_name)
                print 'drug name is %s' % drug_name
                approval_letter_links.append(approval_letter_link)
                print 'link is %s' % approval_letter_link
                match = download_and_parse_letter(approval_letter_link)
                post_marketing_requirements.append(match)
                print 'match is %s' % match
            except: 
                print "something went wrong"
    df = DataFrame({'Drug Names': drug_names,'Approval Letters': approval_letter_links, 'Post Marketing Requirements': post_marketing_requirements})
    df.to_excel('phasefour2011-2014.xlsx', sheet_name='sheet2', index=False)

if __name__ == '__main__':
    get_15_to_19_data()
    #get_11_to_14_data()
    


#2009 to 2010 
#how to generate urls from spreadsheet
# download pdfs into spreadsheet, then traspose and paste in 

#ndas_10 = []
#names_10 = []

#ndas_09 = []
#names_09 = []

#ndas_08 = []
#names_08 = []
#
#ndas_07 = []
#names_07 = []

#ndas_06 = []
#names_06 = []
#
#ndas_05 = []
#ndas_05 = []

#ndas_04 = []
#ndas_04 = []

#ndas_03 = []
#names_03 = []

#ndas_02 = []
#names_02 = []

#ndas_01 = []
#names_01 = []

#ndas_00 = ["N020989","N021014","N020987","N021107","N021084","N020789","N020971","N021119", "N020938","N021130","N021081","N020823","N021174","N021176","N020986",  "N020715","N020883","N020484",  "N020610","N020941","N021214","N021197","N021226","N021248","N020687","N020873","N021204"]

#names_00 = ["Evoxac", "Trileptal", "Protonix", "Lotronex", "Skin Exposure Reduction Paste Against Chemical Warfare Agents", "Zonegran", "Septocaine", "Visudyne", "Mobic", "Zyvox", "Lantus", "Exelon", "Mylotarg", "Welchol", "NovoLog", "Trelstar Depot", "Acova", "Innohep", "Colazal", "Abreva", "Rescula", "Cetrotide", "Kaletra", "Trisenox", "Mifeprex", "Angiomax", "Starlix"]
#
#ndas_99 = ['N020863',	'N020886',	'N020955',	'N021007',	'N020766',	'N021042',	'N021071',	'N020862',	'N021066',	'N021073',	'N021036',	'N021057',	'N021012',	'N021029',	'N020859',	'N020984',	'N020973',	'N021083',	'N050778',	'N050747',	'N021079',	'N020931',	'N020796',	'N020753',	'N021087',	'N020744',	'N021035',	'N020965',	'N020937',	'N020922',	'N021085',	'N021038',	'N021061',	'N020845',	'N021055']

#https://wayback.archive-it.org/7993/20170406061441/https://www.fda.gov/Drugs/DevelopmentApprovalProcess/HowDrugsareDevelopedandApproved/DrugandBiologicApprovalReports/ucm081686.htm

#chose to represent the data as a multidimensional array

#names_99 = ['Pletal','Panretin','Ferrlecit','Agenerase','Xenical', 'Vioxx', 'Avandia',	'Hectorol', 'Zaditor',	'Actos','Relenza',  'Antagon','Neotect',    'Temodar','Sonata','Raplon','Aciphex','Rapamune','Ellence','Synercid IV','Alamast','Tikosyn',   'Comtan',	'Aromasin', 'Tamiflu','Curosurf',	'Keppra',   'Levulan','Optimark',   'Solage','Avelox','Precedex','Tequin','INOmax','Targretin']
#names_numbers_array = np.column_stack((NDAS_99, names_99)) 
#
#for name_number in names_numbers_array:
#    shortened_nda = name_number[0][2:] 
#    drug_url = "https://www.accessdata.fda.gov/drugsatfda_docs/nda/99/%s.cfm" %shortened_nda
#    drug_name = name_number[1]
#    try: 
#        page = urllib2.urlopen(url)
#    except:
        #urls sometimes have underscore followed by drug name
#        backup_url = "https://www.accessdata.fda.gov/drugsatfda_docs/nda/99/%s_%s.cfm" % (shortened_nda, drug_name)
#        page = urllib2.urlopen(backup_url)
#
#    https://www.accessdata.fda.gov/drugsatfda_docs/nda/99/20863.cfm

#import sqlite3
#connection  = sqlite3.connect("test.db")
#cursor      = connection.cursor()
#dropTableStatement = "DROP TABLE phase4watch"
#cursor.execute(dropTableStatement)

