import numpy as np
import pandas as pd
import requests
import json

BASE_URL = "http://www.patentsview.org/api/patents/query?"

def get_patents_by_keywords(keywords_group,ipc_list,year,month):
    """
    Return Dataframe consists of patents whose title
    contains at least one of keywords,
    for specified ipc categories,
    on the given year.
    """

    if month == '12':
        next_month = str(int(year)+1)+'-01'
    else:
        next_month = year+'-'+str(int(month)+1)

    query_year = '{"_gte":{"patent_date":"'+year+'-'+month+'-01"}},\
                   {"_lt":{"patent_date":"'+next_month+'-01"}}'

    num_patents = 0
    patents_df = pd.DataFrame()
    for (section, classification, group) in ipc_list:

        query_section = '{"_eq":{"ipc_section":"'+section+'"}}'
        query_classification = '{"_eq":{"ipc_class":"'+classification+'"}}'
        query_group = '{"_eq":{"ipc_main_group":"'+group+'"}}'

        # 'q={"_and":['+query_year+','+query_section+','+query_classification+','+query_group+']}'
        query = 'q={"_and":['+query_year+','+query_section+','+query_classification+']}'

        output = '&f=["patent_title","patent_number","patent_num_cited_by_us_patents",\
                      "assignee_country", "assignee_organization", "patent_date",\
                      "inventor_first_name", "inventor_last_name", "inventor_id"]'
        option = '&o={"per_page":10000}'

        try:
            r = requests.get(BASE_URL+query+output+option).json()
            num_patents += pd.DataFrame(r).total_patent_count[0]
            if num_patents >= 10000:
                print('Number of patents too big (>10000).')
                return(-1)
            patents_df = pd.concat([patents_df,pd.DataFrame(r)],ignore_index=True)
        except Exception as e:
            print('\nNo patent has been found.')
            return(-1)

    # Clean the Dataframe
    patents_df.reindex(list(range(len(patents_df))))
    columns = ["patent_title","patent_number","patent_num_cited_by_us_patents","assignees",\
               "patent_date", "inventors"]
    patents_df_cleaned = pd.DataFrame(columns=columns)

    for col in columns:
        patents_df_cleaned[col]=list(map(lambda x: x[col], patents_df.patents))

    filter_list = list()
    for title in patents_df_cleaned.patent_title:
        keyword_found = False
        for keyword in keywords_group:
            if keyword in title.lower():
                keyword_found = True
        filter_list += [keyword_found]

    patents_df_cleaned = patents_df_cleaned.loc[filter_list]
    print("Total Patents: %d | Related to AI: %d | Date: %s-%s."\
           %(num_patents, len(patents_df_cleaned), year, month))
    return patents_df_cleaned

def get_num_patents(year,month):

    if month == '12':
        next_month = str(int(year)+1)+'-01'
    else:
        next_month = year+'-'+str(int(month)+1)

    query = 'q={"_and":[{"_gte":{"patent_date":"'+year+'-'+month+'-01"}},\
                        {"_lt":{"patent_date":"'+next_month+'-01"}}]}'

    r = requests.get(BASE_URL+query).json()

    num_patents = pd.DataFrame(r).total_patent_count[0]
    if num_patents > 100000:
        print('Number of patents too big (>10000).')

    print("Total Patents: %d | Date: %s-%s."%(num_patents, year, month))
    return num_patents
