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
from ipywidgets import interact, interactive, fixed, interact_manual

''' N.B: PatentsView.org API does not allow us to get more than 100'000 per request.
    In case there is more than 100'000 patents, we will divide our request into 2 chunks, namely 2 times 6 months,
    if we were to collect patents for a given year. '''

def BASE_URL():
    ''' Returns the base URL of PatentsView website '''
    return 'http://www.patentsview.org/api/patents/query?'

def get_nb_patents_month(month, year):
    ''' Returns the number of patents for a given month of a given year '''
    s = ''
    
    #Special case: if (month == December) we take the patents from December 1st to to January 1st of the following year
    if(month!='12'): 
        s = year+'-'+str(int(month)+1) 
    else:
        s = str(int(year)+1)+'-01'
    #query to be sent
    query = 'q={"_and":[{"_gte":{"patent_date":"'+year+'-'+month+'-01"}},\
        {"_lt":{"patent_date":"'+ s +'-01"}}]}' 
    
    #Sends a GET request and store the data in a JSON file
    r = requests.get(BASE_URL()+query).json()
    #Check if the number of patents obtained is larger than 100'000, which leads to biased result
    if pd.DataFrame(r).total_patent_count[0] > 100000:
        print("Number of patents exceeds 100'000, please take a shorter interval")
    #The total number of patents is contained in every rows of the dataframe (take 0 by default)
    return pd.DataFrame(r).total_patent_count[0]
 

def get_nb_patents_year(year):
    ''' Returns the number of granted patent for a given year (12 months). Uses get_nb_patents_month() to
    add every months together'''
    nb_patent=0
    for i in range(12):
        #Special case, if the month number is less than 10, append a '0'
        if i<10:
            nb_patent+=get_nb_patents_month('0'+str(i), year)
        else:
            nb_patent+=get_nb_patents_month(str(i), year)
    return nb_patent




def get_nb_patent_country(country):
    ''' Requests all the patents of the year 2016 for a given country '''
    ''' Outputs the inventor country for checking purposes '''
    query='q={"_and":[{"_gte":{"patent_date":"2016-01-01"}},\
    {"_lt":{"patent_date":"2017-01-01"}},{"_eq":{"inventor_country":"'+country+'"}}]}' 
    output='&f=["inventor_country"]'
    r = requests.get(BASE_URL()+query+output).json() 

    #Catch an exception in case a given country did not deliver any patent in 2016, i.e. is not cited in the DataBase
    try:
        nb_patents= pd.DataFrame(r).total_patent_count[0] 
        #Special case: The request cannot give more than 100'000 patents, we break the time interval into 2 
        if nb_patents >= 100000: 
            #Send the request for twice 6 month (result always less than 100000)
            query='q={"_and":[{"_gte":{"patent_date":"2016-01-01"}},{"_lt":{"patent_date":"2016-07-01"}},{"_eq":{"inventor_country":"'+country+'"}}]}' 
            r = requests.get(BASE_URL()+query+output).json() 
            #number of patent is countained in every rows of the dataframe            
            nb_patents= pd.DataFrame(r).total_patent_count[0] 
            query='q={"_and":[{"_gte":{"patent_date":"2016-07-01"}},{"_lt":{"patent_date":"2017-01-01"}},{"_eq":{"inventor_country":"'+country+'"}}]}' 
            r = requests.get(BASE_URL()+query+output).json() 
            #Add the 2 requests together
            nb_patents += pd.DataFrame(r).total_patent_count[0] 
    except ValueError: #In case no patents are found
        nb_patents=0   
    return int(nb_patents)



def ret_color(feature, colors):
    ''' Maps each country (precisely its ISO-ALPHA 2 code) to a color depending on the number of patents'''
    if (feature['properties']['iso_a2'] in colors.keys()):
        return colors[feature['properties']['iso_a2']]
    else:
        #Returns the white color if a country does not show up in the list of patents 
        return '#ffffff'

def get_patents(year_start, month_start, year_end, month_end):
    '''Returns the granted patents between the given dates (year and month)'''
    '''Get patent_id, patent_number and patent_title for granted patents between given dates.'''
    
    query='q={"_and":[{"_gte":{"patent_date":"%d-%d-01"}},\
                      {"_lt":{"patent_date":"%d-%d-01"}}]}\
                      &o={"page":1,"per_page":100}' % (year_start, month_start, year_end, month_end)
    return requests.get(BASE_URL() + query).json()



def get_company(year_start, month_start, year_end, month_end ,total_page_num=10):
    ''' Get all the granted patents by companies, between the two given dates'''
    company_total_patent = dict()
    for page_num in range(total_page_num):
        patent_json = get_patents_company(2017, 1, 2017, 5, page_num+1)
        if pd.DataFrame(patent_json).total_patent_count[0] > 100000:
            print("Number of patents exceeds 100'000, please take a shorter interval")
        for patent in patent_json['patents']:
            company_name = patent['assignees'][0]['assignee_organization']
            total_patent =  patent['assignees'][0]['assignee_total_num_patents']
            company_total_patent[company_name] = total_patent
    return company_total_patent



def get_patents_company(year_start, month_start, year_end, month_end, page_num):
    '''Get all granted patents by assignee_organization (company name) and assignee_total_num_patents (number of that companie's patents)
        between given dates.'''
    query='q={"_and":[{"_gte":{"patent_date":"%d-%d-01"}},\
                      {"_lt":{"patent_date":"%d-%d-01"}}]}\
                      &o={"page":%d,"per_page":10000}\
                      &f=["assignee_organization", "assignee_total_num_patents"]'\
                      % (year_start, month_start, year_end, month_end, page_num)
    return requests.get(BASE_URL() + query).json()


# Helper function 
def get_patents_country_sector(year_start, month_start, year_end, month_end, page_num):
    '''Get all granted patents by assignee_organization (company name) and assignee_total_num_patents (number of that companie's patents)
        by sector, using CPC between given dates. (CPC stands for Cooperative Patent Classification)'''
    query='q={"_and":[{"_gte":{"patent_date":"%d-%d-01"}},\
                      {"_lt":{"patent_date":"%d-%d-01"}}]}\
                      &o={"page":%d,"per_page":10000}\
                      &f=["assignee_country", "cpc_group_id"]'\
                      % (year_start, month_start, year_end, month_end, page_num)
    return requests.get(BASE_URL() + query).json()




def get_countries_by_sectors():
    ''' Returns a dictionary that contains categorized patents into sectors,
     for each country, using CPC (Cooperative Patent Classification)'''
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



def fıgure_by_sector(category, label, fig_index, axes, df): 
    ''' Plots the TOP10 countries for a given sector (Categories 'A','B','C', etc.), in terms of the number of granted patents'''
    a = df.sort_values(by=category, ascending=False)
    a.head(10).plot.bar(y=category, figsize=(9,7), fontsize=20, subplots=True, ax=axes[fig_index[0], fig_index[1]], label=label)

category_label = [('A', 'Human Necessities'),('B', 'Operations and Transport'),('C', 'Chemistry and Metallurgys'),('D', 'Textiles'),\
                  ('E', 'Fixed Constructions'),('F', 'Mechanical Engineering'),('G', 'Physics'),('H', 'Electricity'),\
                  ('Y', 'Emerging Cross-Sectional Technologies'),]



def spider_chart(df, index, title=''):
    ''' Draws a spider chart showing the involvment level of a given country in all the 7 sectors in CPC 
        (Cooperative Patent Classification) by showing the relative number of granted patents for each sector, country-wise'''
    labels = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'Y'])

    stats = df.loc[index, labels].values
    angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False) 
  
    stats=np.concatenate((stats,[stats[0]]))  
    angles=np.concatenate((angles,[angles[0]])) 
    
    fig= plt.figure()
    ax = fig.add_subplot(111, polar=True)   # Setting up a polar axis
    ax.plot(angles, stats, 'o-', linewidth=1.5, color='r')  # Draw the plot (or the frame on the radar chart)
    ax.fill(angles, stats, alpha=0.25, color='r') # Fills in the inner area of the spider chart

    labels_ = np.array(['Human Necessities', 'Transport', 'Chemistry',\
                       'Textiles', 'Constructions', 'MechEng',\
                       'Physics', 'Electricity', 'Cross-Sectional Technologies'])

    ax.set_title(title) # The title corresponds to the name of the given country
    ax.set_thetagrids(angles * 180/np.pi, labels_)  #Label the axis using shorter terms
    

#A typical IPC symbol is H01L 31, H=section 01=classification 31=group
#Look at http://www.wipo.int/classifications/ipc/en/ to find the IPC symbols of a category

def query_ipc_by(field, flag):
    query = '{"_or":['
    for i,val in enumerate(field):
        query += '{"_eq":{' + flag + ':"'+ val +'"}}'
        if i != len(field) - 1:
            query += ','
    query += ']}'
    return query

def get_patents_keywords(key_words,year):
    ''' Returns all the patents containing the given keywords, for a given year''' 
    
    #Year query parameters
    query_year = '{"_gte":{"patent_date":"'+year+'-01-01"}},{"_lt":{"patent_date":"'+str(int(year)+1)+'-01-01"}}'
  
    nb_patents=0
    dfPatents=pd.DataFrame()
    #Send a query for every keyword
    for i in key_words:         
        query_key_words='{"_text_phrase":{"patent_title":"'+i+'"}}'
        query='q={"_and":['+query_year+','+query_key_words+']}' 
        output='&f=["patent_title","patent_number"]' 
        
        #Exception handler in case no patent is found for a given keyword
        try:
            r = requests.get(BASE_URL()+query+output).json()
            nb_patents+=pd.DataFrame(r).total_patent_count[0] 
            dfPatents=pd.concat([dfPatents,pd.DataFrame(r)])
        except ValueError:
            pass   
    return dfPatents, nb_patents

#Get patents by IPC, and then filter them by keywords                                                                       (used for FinTech)
def get_patents_keywords_ipc(keywords, year, list_ipc):
    ''' Returns all the patents containing the given keywords, for a given year'''

    #Year query parameters
    query_year = '{"_gte":{"patent_date":"'+year+'-01-01"}},{"_lt":{"patent_date":"'+str(int(year)+1)+'-01-01"}}'

    nb_patents=0
    dfPatents=pd.DataFrame()
    #Send a query for every keyword
    for (section, classification, group) in list_ipc:
        query_group = '{"_eq":{"ipc_main_group":"'+group+'"}}'
        query_section = '{"_eq":{"ipc_section":"'+section+'"}}'
        query_classification = '{"_eq":{"ipc_class":"'+classification+'"}}'
        
        query='q={"_and":['+query_year+','+query_section+','+query_classification+','+query_group+']}'
        output='&f=["patent_title","patent_number","ipc_section","ipc_main_group","ipc_class","patent_num_cited_by_us_patents",\
                      "assignee_country", "assignee_organization", "patent_date",\
                      "inventor_first_name", "inventor_last_name", "inventor_id"]'


        option='&o={"per_page":10000}'
        #Exception handler in case no patent is found for a given keyword
        try:
            r = requests.get(BASE_URL()+query+output+option).json()
            nb_patents+=pd.DataFrame(r).total_patent_count[0]
            dfPatents=pd.concat([dfPatents,pd.DataFrame(r)],ignore_index=True)
        except ValueError:
            pass

    #Clean the dataframe
    dfPatents.reindex(list(range(len(dfPatents))))
    
    columns = ["patent_title","patent_number", "IPCs", "patent_num_cited_by_us_patents","assignees",\
               "patent_date", "inventors"]

    dfPatents_cleaned=pd.DataFrame(columns=columns)
    for col in columns:
        dfPatents_cleaned[col]=list(map(lambda x: x[col], dfPatents.patents))

    
    filter_list=[]
    keyWordFound=False
    for title in dfPatents_cleaned.patent_title:
        for tuple_keyword in keywords:
            for i in range(len(tuple_keyword)):
                if tuple_keyword[i] not in title:
                    keyWordFound=False
                    break                  
                if i == len(tuple_keyword)-1:
                    keyWordFound=True                    
            if keyWordFound==True:
                break
        filter_list.append(keyWordFound)
     
    dfPatents_cleaned = dfPatents_cleaned.loc[filter_list]
    return dfPatents_cleaned, len(dfPatents_cleaned)


##########################################################################################
#                    THIS FUNCTION IS USELESS
##########################################################################################

def get_patents_keywords_fil(key_words, year, section, classification, group):
    ''' Returns all the patents containing the given keywords, for a given year'''

    #Year query parameters
    query_year = '{"_gte":{"patent_date":"'+year+'-01-01"}},{"_lt":{"patent_date":"'+str(int(year)+1)+'-01-01"}}'

    #Query all the three IPC parts
    query_section = query_by(section, "ipc_section")
    query_classification = query_by(classification, "ipc_class")
    query_group = query_by(group, "ipc_main_group")

    nb_patents=0
    dfPatents=pd.DataFrame()
    
    #Query each keyword
    for i in key_words:
        query_key_words='{"_text_phrase":{"patent_title":"'+i+'"}}'
        query='q={"_and":['+query_year+','+query_key_words+','+query_section+','+query_classification+','+query_group+']}'
        output='&f=["patent_title","patent_number","ipc_section","ipc_main_group","ipc_class"]'
        option='&o={"per_page":10000}'
        #Exception handler in case no patent is found for a given keyword
        try:
            r = requests.get(BASE_URL()+query+output+option).json()
            nb_patents+=pd.DataFrame(r).total_patent_count[0]
            if nb_patents > 10000:
                print('nb of patents too big (>10000)')
            dfPatents=pd.concat([dfPatents,pd.DataFrame(r)],ignore_index=True)
        except ValueError:
            pass

    #Clean the dataframe
    dfPatents.reindex(list(range(len(dfPatents))))
    columns = ["patent_title","patent_number","IPCs"]
    dfPatents_cleaned=pd.DataFrame(columns=columns)
    for col in columns:
        dfPatents_cleaned[col]=list(map(lambda x: x[col], dfPatents.patents))

    return [dfPatents_cleaned, nb_patents]

##########################################################################################


#A typical IPC symbol is H01L 31, H=section 01=classification 31=group
#Look at http://www.wipo.int/classifications/ipc/en/ to find the IPC symbols of a category

#Used for solar energy part (by IPC)
def get_patents_keywords_ipc_sk(key_words1, key_words2, year, section, classification, group):
    ''' Returns all the patents containing the given keywords, for a given year'''

    #Year query parameters
    query_year = '{"_gte":{"patent_date":"'+year+'-01-01"}},{"_lt":{"patent_date":"'+str(int(year)+1)+'-01-01"}}'

    query_section = query_by(section, "ipc_section")
    query_classification = query_by(classification, "ipc_class")
    query_group = query_by(group, "ipc_main_group")

    nb_patents=0
    dfPatents=pd.DataFrame()
    #Send a query for every keyword
    for i in key_words1:
        for j in key_words2:
            query_key_words='{"_and":[{"_text_phrase":{"patent_title":"'+i+'"}},{"_text_phrase":{"patent_title":"'+j+'"}}]}'
            query='q={"_and":['+query_year+','+query_key_words+','+query_section+','+query_classification+','+query_group+']}'
            output='&f=["patent_title","patent_number","ipc_section","ipc_main_group","ipc_class"]'
            option='&o={"per_page":10000}'
            #Exception handler in case no patent is found for a given keyword
            try:
                r = requests.get(BASE_URL()+query+output+option).json()
                nb_patents+=pd.DataFrame(r).total_patent_count[0]
                dfPatents=pd.concat([dfPatents,pd.DataFrame(r)],ignore_index=True)
            except ValueError:
                pass

    #Clean the dataframe
    dfPatents.reindex(list(range(len(dfPatents))))
    columns = ["patent_title","patent_number","IPCs"]
    dfPatents_cleaned=pd.DataFrame(columns=columns)
    for col in columns:
        dfPatents_cleaned[col]=list(map(lambda x: x[col], dfPatents.patents))

    return [dfPatents_cleaned, nb_patents]


def get_nb_patent_years_keyword(years,keywords,list_ipc):
    list_patent_nb = []
    df = pd.DataFrame()
    for i in years:
        if (i != 2005): 
            dfPatent, nb_patent = get_patents_keywords_ipc(keywords,str(i),list_ipc)
            list_patent_nb.append(nb_patent)
            df= pd.concat([df,dfPatent],ignore_index=True)
    return list_patent_nb, df


def plt_nb_patent(x,y,x_axis,y_axis,title):
    plt.plot(x,y)
    plt.xlabel(x_axis)
    plt.ylabel(y_axis)
    plt.title(title)
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)


def savedfexcel(df, excel_title):
    writer = pd.ExcelWriter('{0}.xlsx'.format(excel_title))
    df.to_excel(writer,'Sheet1')
    writer.save()


def get_growth(years, list_nb_patents):
    growth=[]
    for i in range(len(years)-1):
        growth+=[(list_nb_patents[i+1]-list_nb_patents[i])/list_nb_patents[i]*100]
    return growth


def build_dataframe(years,keywords,list_ipc):
    list_patent_nb=[]
    dfPatents=pd.DataFrame()
    for i in years:
        [dfPatentsYear, nb_patent]=get_patents_keywords_energy(keywords,str(i),list_ipc)
        dfPatentsYear['year']=i
        dfPatents=pd.concat([dfPatentsYear,dfPatents],ignore_index=True)
        dfPatents.set_index([list(range(len(dfPatents)))],inplace=True)
    return dfPatents


def df_get_nb_by_group_and_clean(df, group, years, showtotal=False):
    dfcopy=df.copy()
    dfcopy['nb patent']=1
    dfpatentgroup = dfcopy.groupby(['year',group]).sum()
    dfpatentgroup=dfpatentgroup.unstack(level=1).fillna(0)
    dfpatentgroup.sort_values(by=years,axis=1, ascending=False,inplace=True)
    dfpatentgroup_copy=dfpatentgroup.transpose().copy()
    dfpatentgroup_copy['total'] = dfpatentgroup_copy.apply(sum, axis=1)
    dfpatentgroup_copy.reset_index(inplace=True)
    dfpatentgroup_copy.drop('level_0', axis=1, inplace=True)
    dfpatentgroup_copy.set_index(group, inplace=True)

    if showtotal==False:
        clean_df = dfpatentgroup_copy.sort_values(by='total', ascending=False).drop('total',axis=1)
    else:
        clean_df = dfpatentgroup_copy.sort_values(by='total', ascending=False)
    return clean_df

def read_df(PATH):
    return pd.read_excel(PATH + '.xlsx')

def plt_interactive_by_country(sector):
    
    feature = 'inventor_country'
    years=list(range(2010,2017))

    if sector == 'solar photo':
        df=df_get_nb_by_group_and_clean(read_df('patent_solar_photo'), feature, years, False).head(10)
    if sector == 'solar termal':
        df=df_get_nb_by_group_and_clean(read_df('patent_solar_thermo'), feature, years, False).head(10)
    if sector == 'wind':
        df=df_get_nb_by_group_and_clean(read_df('patent_wind'), feature, years, False).head(10)
    if sector == 'hydro':
        df=df_get_nb_by_group_and_clean(read_df('patent_hydro'), feature,years, False).head(10)
    if sector == 'tidal and wave':
        df=df_get_nb_by_group_and_clean(read_df('patent_wave_tidal'), feature,years, False).head(10)
    if sector == 'carbon capture':
        df=df_get_nb_by_group_and_clean(read_df('patent_carbon_storage'), feature,years, False).head(10)
    if sector == 'renewable':
        df=df_get_nb_by_group_and_clean(read_df('patent_renewable'), feature, years, False).head(10)       
    df.plot.barh(stacked=True, fontsize=20, figsize=(20,13), rot=0, grid=True)
    plt.show()




def plt_interactive_by_company(sector):
    
    feature = 'assignee_organization'
    years=list(range(2010,2017))

    if sector == 'solar photo':
        df=df_get_nb_by_group_and_clean(read_df('patent_solar_photo'), feature, years, False).head(10)
    if sector == 'solar termal':
        df=df_get_nb_by_group_and_clean(read_df('patent_solar_thermo'),feature, years, False).head(10)
    if sector == 'wind':
        df=df_get_nb_by_group_and_clean(read_df('patent_wind'),feature, years, False).head(10)
    if sector == 'hydro':
        df=df_get_nb_by_group_and_clean(read_df('patent_hydro'), feature,years, False).head(10)
    if sector == 'tidal and wave':
        df=df_get_nb_by_group_and_clean(read_df('patent_wave_tidal'), feature,years, False).head(10)
    if sector == 'carbon capture':
        df=df_get_nb_by_group_and_clean(read_df('patent_carbon_storage'), feature,years, False).head(10)
    if sector == 'renewable':
        df=df_get_nb_by_group_and_clean(read_df('patent_renewable'), feature, years, False).head(10)       
    df.plot.barh(stacked=True, fontsize=20, figsize=(20,13), rot=0, grid=True)
    plt.show()


def get_patents_keywords_energy(keywords,year, list_ipc):
    ''' Returns all the patents containing the given keywords, for a given year'''

    #Year query parameters
    query_year = '{"_gte":{"patent_date":"'+year+'-01-01"}},{"_lt":{"patent_date":"'+str(int(year)+1)+'-01-01"}}'

    nb_patents=0
    dfPatents=pd.DataFrame()
    #Send a query for every keyword
    for (section, classification, group) in list_ipc:
        query_group = '{"_eq":{"ipc_main_group":"'+group+'"}}'
        query_section = '{"_eq":{"ipc_section":"'+section+'"}}'
        query_classification = '{"_eq":{"ipc_class":"'+classification+'"}}'

        query='q={"_and":['+query_year+','+query_section+','+query_classification+','+query_group+']}'
        output='&f=["patent_title","inventor_country","assignee_organization","patent_number"]'
        option='&o={"per_page":10000}'
        #Exception handler in case no patent is found for a given keyword
        try:
            r = requests.get(BASE_URL()+query+output+option).json()
            nb_patents+=pd.DataFrame(r).total_patent_count[0]
            if nb_patents > 10000:
                print('nb of patents too big (>10000)')
            dfPatents=pd.concat([dfPatents,pd.DataFrame(r)],ignore_index=True)
        except ValueError:
            pass

    #Clean the dataframe
    dfPatents.reindex(list(range(len(dfPatents))))

    columns = ["patent_title","patent_number","inventor_country","assignee_organization"]
    dfPatents_cleaned=pd.DataFrame(columns=columns)

    for col in columns:
        if col == 'inventor_country':
            dfPatents_cleaned[col]=list(map(lambda x: x['inventors'][0][col], dfPatents.patents))
        elif col == 'assignee_organization':
            dfPatents_cleaned[col]=list(map(lambda x: x['assignees'][0][col], dfPatents.patents))
        else:
            dfPatents_cleaned[col]=list(map(lambda x: x[col], dfPatents.patents))
            
    filter_list=[]
    keyWordFound=False
    for title in dfPatents_cleaned.patent_title:
        for tuple_keyword in keywords:
            for i in range(len(tuple_keyword)):
                if tuple_keyword[i] not in title:
                    keyWordFound=False
                    break
                if i == len(tuple_keyword)-1:
                    keyWordFound=True
            if keyWordFound==True:
                break
        filter_list+=[keyWordFound]

    dfPatents_cleaned = dfPatents_cleaned.loc[filter_list]
    return [dfPatents_cleaned, len(dfPatents_cleaned)]

def get_nb_patent_years_keyword_energy(years,keywords,list_ipc):
    list_patent_nb=[]
    for i in years:
        [dfPatent, nb_patent]=get_patents_keywords_energy(keywords,str(i),list_ipc)
        list_patent_nb+=[nb_patent]
    return list_patent_nb