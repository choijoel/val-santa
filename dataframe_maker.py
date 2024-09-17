from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

#soup = BeautifulSoup(html_doc, 'html.parser')
#element = soup.find("div", class_="trn-match-row__text-value").get_text()
#print(soup.get_text())
#print(element)

###new soup element, trying to access html with the tags

def dfer (html_name):
    HTMLfile = open(html_name, 'r')

    index = HTMLfile.read()

    stew = BeautifulSoup(index, 'html.parser')

    '''one_stat = stew.find("div", class_="trn-match-row__text-value")
    print(one_stat.get_text())
    print(one_stat)

    # stew.div = one_stat <-- one_stat alr has div included
    tag_name = one_stat['class']
    print (tag_name)'''

    'trn-match-row__text-label'

    #finds and makes the labels for the dataframe
    tracker_label = []

    #finds and adds data of stats to each label
    tracker_data = []
    count = 0


    for divs in stew.find_all("div"):
        #finds every instance of div until the break in for loop
        stats = divs.get_text()
        try:
            stat_class = divs['class']
            #stat_class returns the class name of the div in an array of each word
            #if the first word of the div is trn-match-header(the headings of each day of matches), or vmr (the matches themselves) it adds it to tracker_label
            #once it gets to the next set of matches/match it breaks the for loop
            if ((stat_class[0] == 'vmr' or stat_class[0] == 'trn-match-header') and count > 0):
                break

            #when the count equals 1, that signifies the start of a header/matches and the need to collect the labels of one heading and one match
            elif (stat_class[0] == 'vmr'  and count <= 0):
                count += 1

            elif (stat_class[0] == 'trn-match-row__text-label'):
                #bc one the headers were weird and it happened to be the longest label so we cut out the weird part
                tracker_label.append(stats[0:11])
        
        except:
            pass

    #making a dataframe with the text of each div in the header/matches
    df = pd.DataFrame(columns = tracker_label)
    #also, the number of columns is 12 but the number of data entries is 13. 
    #this is b/c one of the datum (divs.get_text(), the rounds won or lost) did not have a corresponding divs['class']

    #creates an empty array so that the data from the tracker can be added to the dataframe as a row
    empty = ['' for _ in range (20)]
    empty.clear()


    #just to see if empty works
    '''
    for i in range(len(empty)) :
        if(i < len(tracker_label)):
            empty[i] = tracker_label[i]
        else:
            break
    '''
    empty.clear()


    for divs in stew.find_all("div"):
        stats = divs.get_text()
        try:
            stat_class = divs['class'] 
            #remind, uses index 0 becuase ['class'] returns a list of items
            if (stat_class[0] == 'vmr' or stat_class[0] == 'trn-match-row__section'):
                #12 is the length of tracker_label and number of columns
                #resets the empty list
                empty = [0 for _ in range (12)]
            #why need >6? first, tracker data adds data of one of two things: the data in the header or the data in a match
            #the data in the match is like 7, so when its match data, we shift it to one end of df
            #bc the columns in the df are labeled as [header_label1, header_label2...] and then [match_label1, match_label2...]
                if(len(tracker_data) > 6):
                    for i in range(len(empty)) :
                        if(i< len(tracker_data)):
                            empty[i+4] = tracker_data[i]
                        else:
                            pass
                else:
                    for i in range(len(empty)) :
                        if(i < len(tracker_data)):
                            empty[i] = tracker_data[i]
                        else:
                            pass

                '''
                print(tracker_label)
                tracker_label.clear()
                print(tracker_data)
                tracker_data.clear()
                '''
                #adds the data to the dataframe
                #note, the data from the header and data from matches are formed separately/in diff iterations
                length = len(df)
                df.loc[(length)] = empty
                #resets the tracker_data list so new data can be added to the next row of df
                tracker_data.clear()
                '''
                print(count)
                length = len(df.index)
                df.loc[count] = tracker_data
                print(length)
                print(len(tracker_data))
                tracker_data.clear()
                print('z')
                print(tracker_data)
                count += 1
            
                tracker_stat = []
                elif (stat_class[0] == 'trn-match-row__text-value'):
                            tracker_stat.append(divs)'''
            

            if(stat_class[0] == 'trn-match-row__text-value'):
                tracker_data.append(stats)
            #mismatch between lists, when label is competitive (1 points) data has map name, and score (2 points)


        except:
            pass
        






    df.columns =['avgK/D', 'avgDDI', 'avgHS%', 'avgADR', 'avgACS/Map', 'Rounds W/L', 'K / D / A', 'K/D', 'DDI', 'HS%', 'ADR', 'ACS']
    #print(list(df.columns))
    total_rounds = []
    df['ADR']=df['ADR'].astype(float)
    df['ACS']=df['ACS'].astype(float)
    df['K/D']=df['K/D'].astype(float)
    df['DDI']=df['DDI'].astype(float)
    df['HS%']=df['HS%'].astype(float)


    #print(df.dtypes)
    for i in range(len(df)):
        word = df['Rounds W/L'][i]
        #print(type(word))
        #print(word)
        if(type(word) == str):
            colon = word.find(':')
            sum = (float(word[:colon])) + (float(word[colon+1:]))
        else:
            sum = float(word)

        total_rounds.append(sum)
    df["Total Rounds"] = total_rounds



    match_data = []
    avg_data = []
    not_match_data = []
    for i in range(len(df)):
        if (df.loc[i , 'Rounds W/L'] == 0):
            not_match_data.append(i)
            #future: remove row
        elif (df.loc[i , 'avgK/D'] != 0):
            avg_data.append(i)
            #future: add to a new data frame for only averages, remember the indexes in another column, then remove from this dataframe
        elif (df.loc[i , 'Rounds W/L'] != 0):
            match_data.append(i)


    avg_df = df.iloc[avg_data, 1:5]


    #dataframe of averages

    #match_df = df.drop(index = not_match_data)
    #match_df = match_df[match_df['Rounds W/L'] != 0]

    match_df = df.iloc[match_data, 4:13]
    #print(len(df.columns)) = 13
    #makes dataframe of only matches
    ###match_df.rename(columns = {'avgACS/Map' : "Map"})
    #future: remove the first column up until maps 


    # note - the indexes are weird because they are still connected to original df. 
    # changing one val in df (the original df)
    # will change it in mathc_df i believe, not other way around tho (maybe? perhaps changing data in one
    # will change it in the other)
    # if u want to have them unaffected, use df.copy

    #ok so not true, it doesn't change the stuff in df
    #also this goddamn rename isn't working for the fookin match_df
    #but for some reason this it works for df but not when i print it only when it 
    #fookin shows up in this line when i never printed it??????
    #i swear im not trippin

    #have to use inplace=True if want to modify current df, else equal it to another df

    match_df.rename(columns={'avgACS/Map': 'Map'}, inplace = True)

    match_df.rename(columns = {'K / D / A' : "kda"}, inplace = True)
    #match_df.rename(columns = {'ACS' : "acs"}, inplace = True)
    
    '''for i in match_df.index:
        word = match_df['K / D / A'][i]
        print(word)
        print(type(word))
        #have to assign match_df to new_df or the changes will not show up in match_df, only new_df
        new_df = match_df.assign(Deaths= word.split('/')[1])
        print(word.split('/')[1])
        print(new_df['Deaths'][i])'''
    
    ##adds a new column only acquiring deaths from kda
    new_df = match_df.assign(Deaths=match_df['kda'].str.split("/").str.get(1))
    new_df['Deaths']=new_df['Deaths'].astype(float)
    new_df.sort_values(['ACS'], inplace=True)

    #df.rename(columns={'avgACS/Map': 'Map'})
    #match_df.at[3 , 'avgACS/Map'] = 'Haven'


    ##new dataframe of some simple stats of ACS grouped by Map
    map_df = new_df.groupby("Map").ACS.agg(['count','mean', 'std', "min", 'max'])

    ## ok

    #%matplotlib

    ##have to ouput match_df and df somewhere

    new_df.reset_index(drop = True, inplace=True)

    #avg_acs = new_df.ACS.mean()


    """
    fig = new_df.plot.scatter(x = 'Total Rounds', y = 'ACS', title = HTMLfile.name[:-5], figsize=(20,16), fontsize=(26)).get_figure()
    ax = plt.gca()
    ax.set_xlim([0, 40])
    ax.set_ylim([0, 400])"""

    plt.figure()
    fig = new_df['ACS'].plot.hist(alpha=0.5, bins = 7, title = HTMLfile.name[:-5], figsize=(20,16), fontsize=(25)).get_figure()
    fig.savefig(html_name[:-5] + '.png')
    



    return {"match":new_df, "map":map_df}


#match_df.to_excel("path_to_file.xlsx", sheet_name = HTMLfile.name[:-5])






print('done')


## can make this whole thing a function where you input the filename and it returns a dataframe
# then you could create multiple sheets in one excel file