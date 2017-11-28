import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import os
import seaborn as sns 
import requests
from bs4 import BeautifulSoup
import folium
import json
import branca.colormap as cm


def BASE_URL():
    return 'http://www.patentsview.org/api/patents/query?'

#The following function return the number of patents for a given month in a given year
def get_nb_patents_month(month, year):
    s = ''
    #Special case : if month= december take from first of december to first of january next year
    if(month!='12'): 
        s = year+'-'+str(int(month)+1) 
    else:
        s = str(int(year)+1)+'-01'
    query = 'q={"_and":[{"_gte":{"patent_date":"'+year+'-'+month+'-01"}},\
        {"_lt":{"patent_date":"'+ s +'-01"}}]}' 
    #Send the request
    r = requests.get(BASE_URL()+query).json()
    #Check if the number of patents obtains is larger than 100000 which involves a wrong result
    if pd.DataFrame(r).total_patent_count[0] > 100000:
        print("number of patent innacurate because greater than 100000")
    return pd.DataFrame(r).total_patent_count[0]



# The following function return the number of granted patent for a given year.
# The previous funcion get_nb_patents_month is used and the every month in the year are added together
def get_nb_patents_year(year):
    nb_patent=0
    for i in range(12):
        #Special case, if the month number is less than 10, send "0x" with x = month number
        if i<10:
            nb_patent+=get_nb_patents_month('0'+str(i), year)
        else:
            nb_patent+=get_nb_patents_month(str(i), year)
    return nb_patent




def get_nb_patent_country(country):
    #Request for the year 2016 and a given country
    #Output the inventor country for checking purpose
    query='q={"_and":[{"_gte":{"patent_date":"2016-01-01"}},\
    {"_lt":{"patent_date":"2017-01-01"}},{"_eq":{"inventor_country":"'+country+'"}}]}' 
    output='&f=["inventor_country"]'
    r = requests.get(BASE_URL()+query+output).json() 

    #Catch an exception for the case a given country did not delivered any patent in 2016 
    try:
        nb_patents= pd.DataFrame(r).total_patent_count[0] 
        #Special case (the request cannot give more than 100'000 results)
        if nb_patents >= 100000: 
            query='q={"_and":[{"_gte":{"patent_date":"2016-01-01"}},{"_lt":{"patent_date":"2016-07-01"}},{"_eq":{"inventor_country":"'+country+'"}}]}' 
            r = requests.get(BASE_URL()+query+output).json() 
            nb_patents= pd.DataFrame(r).total_patent_count[0] 
            query='q={"_and":[{"_gte":{"patent_date":"2016-07-01"}},{"_lt":{"patent_date":"2017-01-01"}},{"_eq":{"inventor_country":"'+country+'"}}]}' 
            r = requests.get(BASE_URL()+query+output).json() 
            nb_patents += pd.DataFrame(r).total_patent_count[0] 
    except ValueError:
        nb_patents=0   
    return int(nb_patents)



def ret_color(feature, colors):
    if (feature['properties']['iso_a2'] in colors.keys()):
        return colors[feature['properties']['iso_a2']]
    else:
        #Return the white color if the country does not show up in the list of patents 
        return '#ffffff'

'''This function returns the granted patents between the given dates'''
def get_patents(year_start, month_start, year_end, month_end):
    '''Get patent_id, patent_number and patent_title for granted patents between given dates.'''
    
    query='q={"_and":[{"_gte":{"patent_date":"%d-%d-01"}},\
                      {"_lt":{"patent_date":"%d-%d-01"}}]}\
                      &o={"page":1,"per_page":100}' % (year_start, month_start, year_end, month_end)
    return requests.get(BASE_URL() + query).json()



# GET COMPANY AND TOTAL PATENT COUNT
def get_company(year_start, month_start, year_end, month_end ,total_page_num=10):
    company_total_patent = dict()
    for page_num in range(total_page_num):
        patent_json = get_patents_company(2017, 1, 2017, 5, page_num+1)
        if pd.DataFrame(patent_json).total_patent_count[0] > 100000:
            print("number of patent innacurate because greater than 100000")
        for patent in patent_json['patents']:
            company_name = patent['assignees'][0]['assignee_organization']
            total_patent =  patent['assignees'][0]['assignee_total_num_patents']
            company_total_patent[company_name] = total_patent
    return company_total_patent



def get_patents_company(year_start, month_start, year_end, month_end, page_num):
    '''Get assignee_organization and assignee_total_num_patents for patents granted between given dates.'''
    query='q={"_and":[{"_gte":{"patent_date":"%d-%d-01"}},\
                      {"_lt":{"patent_date":"%d-%d-01"}}]}\
                      &o={"page":%d,"per_page":10000}\
                      &f=["assignee_organization", "assignee_total_num_patents"]'\
                      % (year_start, month_start, year_end, month_end, page_num)
    return requests.get(BASE_URL() + query).json()


# Helper function 
def get_patents_country_sector(year_start, month_start, year_end, month_end, page_num):
    '''Get assignee_organization and assignee_total_num_patents for patents granted between given dates.''' 
    query='q={"_and":[{"_gte":{"patent_date":"%d-%d-01"}},\
                      {"_lt":{"patent_date":"%d-%d-01"}}]}\
                      &o={"page":%d,"per_page":10000}\
                      &f=["assignee_country", "cpc_group_id"]'\
                      % (year_start, month_start, year_end, month_end, page_num)
    return requests.get(BASE_URL() + query).json()




# GET COUNTRY AND TOTAL PATENT COUNT IN SECTORS
def get_countries_by_sectors():
    country_total_patent_category = dict()
    total_page_num = 3
    for i in range(11):
        for page_num in range(total_page_num):
            patent_json = get_patents_country_sector(2016, i+1, 2016, i+2, page_num+1)
            if patent_json['patents'] != None:
                for patent in patent_json['patents']:
                    country = patent['assignees'][0]['assignee_country']
                    patent_categories = patent['cpcs']
                    for category in patent_categories:
                        if country and category['cpc_group_id']:
                            code = category['cpc_group_id'][0]
                            if country in country_total_patent_category:
                                if code in country_total_patent_category[country]:
                                    country_total_patent_category[country][code] += 1
                                else:
                                    country_total_patent_category[country][code] = 1
                            else:
                                country_total_patent_category[country] = dict()
                                country_total_patent_category[country][code] = 1
    return country_total_patent_category


# Plot the top 10 countries in terms of number of patents, by country
def fıgure_by_sector(category, label, fig_index, axes, df): 
    a = df.sort_values(by=category, ascending=False)
    a.head(10).plot.bar(y=category, figsize=(9,7), fontsize=20, subplots=True, ax=axes[fig_index[0], fig_index[1]], label=label)

category_label = [('A', 'Human Necessities'),('B', 'Operations and Transport'),('C', 'Chemistry and Metallurgys'),('D', 'Textiles'),\
                  ('E', 'Fixed Constructions'),('F', 'Mechanical Engineering'),('G', 'Physics'),('H', 'Electricity'),\
                  ('Y', 'Emerging Cross-Sectional Technologies'),]




def figure_by_sector(category, label, fig_index):
    '''This function draws barplots the top 10 countries in terms of number of patents, by sectors'''
    top_countries_df = patent_category_df.sort_values(by=category, ascending=False)
    top_countries_df.head(10).plot.bar(y=category, figsize=(9,7), fontsize=20, subplots=True, ax=axes[fig_index[0], fig_index[1]], label=label)

category_label = [('A', 'Human Necessities'),('B', 'Operations and Transport'),('C', 'Chemistry and Metallurgys'),('D', 'Textiles'),\
                  ('E', 'Fixed Constructions'),('F', 'Mechanical Engineering'),('G', 'Physics'),('H', 'Electricity'),\
                  ('Y', 'Emerging Cross-Sectional Technologies'),]
    


def draw_radar_graph(df, index,
                    title='', sub_ = 111):
    labels = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Y'])
    labels_ = np.array(['Human Necessities', 'Transport', 'Chemistry',\
                       'Textiles', 'Constructions', 'MechEng',\
                       'Physics', 'Electricity', 'Cross-Sectional Technologies'])

    stats = df.loc[index, labels].values
    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False) # Set the angle
    
    # close the plot
    stats=np.concatenate((stats,[stats[0]]))  # Closed
    angles=np.concatenate((angles,[angles[0]]))  # Closed
    
    fig= plt.figure()
    ax = fig.add_subplot(111, polar=True)   # Set polar axis
    ax.plot(angles, stats, 'o-', linewidth=2, color='r')  # Draw the plot (or the frame on the radar chart)
    ax.fill(angles, stats, alpha=0.25, color='r')  #Fulfill the area
    ax.set_thetagrids(angles * 180/np.pi, labels_)  # Set the label for each axis
    ax.set_title(title)
    return ax

def get_patents_keywords(key_words,year):
    #Year query parameters
    query_year = '{"_gte":{"patent_date":"'+year+'-01-01"}},{"_lt":{"patent_date":"'+str(int(year)+1)+'-01-01"}}'
  
    nb_patents=0
    dfPatents=pd.DataFrame()
    #Send a query for every key words
    for i in key_words:         
        query_key_words='{"_text_phrase":{"patent_title":"'+i+'"}}'
        query='q={"_and":['+query_year+','+query_key_words+']}' 
        output='&f=["patent_title","patent_number"]' 
        #Exception manager in case no patents are found for a given key word
        try:
            r = requests.get(BASE_URL()+query+output).json()
            nb_patents+=pd.DataFrame(r).total_patent_count[0] 
            dfPatents=pd.concat([dfPatents,pd.DataFrame(r)])
        except ValueError:
            pass   
    return [dfPatents, nb_patents]