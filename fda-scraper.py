#!/bin/env pytho/bin/env python -m pip install --upgrade mymodulen
import urllib.request
import re
import numpy as np
from pandas import DataFrame
from bs4 import BeautifulSoup
import PyPDF2
import code

drug_names = []
approval_letter_links = []
post_marketing_requirements = []

def get_2015_to_2019_data():
    
    years = [2015, 2016, 2017, 2018, 2019]

#for each year, find pdfs, parse for requirements, add to dataframe, write to excel

    for year in years:
        all_drug_links_for_year = get_links_for_year(year)

        for individual_drug_url in all_drug_links_for_year:
            approval_letter = get_approval_letter_for_drug(individual_drug_url)
            parse_letter_for_requirements(approval_letter)
    
    # put data in dataframe and write to csv
    df = DataFrame({'Drug Names': drug_names,
                   'Approval Letters': approval_letter_links,
                   'Post Marketing Requirements': post_marketing_requirements})
    df.to_excel('phasefour.xlsx', sheet_name='2015-2019', index=False)

def get_links_for_year(year):
    all_drugs_for_year_url = \
            'https://www.fda.gov/drugs/new-drugs-fda-cders-new-molecular-entities-and-new-therapeutic-biological-products/novel-drug-approvals-%s' \
            % year
    page = urllib.request.urlopen(all_drugs_for_year_url)
    page_html = BeautifulSoup(page, 'html.parser')
    table = page_html.find('table')
    table_body = table.find('tbody')
    drug_links = table_body.find_all('a',
        href=re.compile('accessdata'))
    return drug_links

def get_approval_letter_for_drug(individual_drug_url):

    drug_name = individual_drug_url.string
    try:
        page = urllib.request.urlopen(individual_drug_url['href'])
        page_html = BeautifulSoup(page, 'html.parser')
        approval_letter = page_html.find('a', text='Letter (PDF)')
        approval_letter_link = approval_letter['href']
        approval_letter = urllib.request.urlretrieve(approval_letter_link,'approval_letter')
        letter_pdf = PyPDF2.PdfFileReader('approval_letter')
        drug_names.append(drug_name)
        approval_letter_links.append(approval_letter_link)
        return letter_pdf
    except:
        print('something went wrong for %s' % drug_name)

def parse_letter_for_requirements(letter_pdf):
    NumPages = letter_pdf.getNumPages()
    postmarketing_string = 'postmarketing'
    # code.interact(local=dict(globals(), **locals()))
    has_requirement = False
    for i in range(0, NumPages):
        PageObj = letter_pdf.getPage(i)
        Text = PageObj.extractText()
        ResSearch = re.search(postmarketing_string, Text)
        if str(ResSearch) != 'None':
            has_requirement = True
            break
    post_marketing_requirements.append(has_requirement)
            

if __name__ == '__main__':
    get_2015_to_2019_data()
    


