from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import os
import xlsxwriter

from dataframe_maker import dfer

df_list = []
name_list = []
map_list = []

folder_path = r'C:\Users\\python stuff\tracker_files'
prev_path = r'C:\Users\\python stuff'

list_of_files = os.listdir(folder_path)
os.chdir(folder_path)
for name in list_of_files:
    if name.endswith(('.html', '.htm')):
        print(name)
        print(os.getcwd())
        df_list.append(dfer(name).get("match"))
        map_list.append(dfer(name).get("map"))
        #dfer(name).get("name_of_return")
        name_list.append(name)


os.chdir(prev_path)
all_df = pd.concat(df_list, ignore_index = True , sort = False)
avg_acs = all_df["ACS"].mean()
mort_rate = all_df["Deaths"].sum() / all_df['Total Rounds'].sum()

with pd.ExcelWriter("path_to_file.xlsx", engine = 'xlsxwriter') as writer:
#the 'with" thing makes it so the excelwriter and writer object(?) is only active for this section/loop
#which is prob why u don't need to close it by using writer.save() or writer.close()
    workbook = writer.book
    for i,(df, df2) in enumerate(zip(df_list, map_list)):
        namer = name_list[i][:-5]
        worksheet=workbook.add_worksheet(namer)
        #adds a sheet called namer
        iort_rate = df["Deaths"].sum() / df['Total Rounds'].sum()
        acsie = df["ACS"].mean()
        adrie = df["ADR"].mean()

        mort_df = pd.DataFrame({namer : iort_rate, "Total Avg": mort_rate}, index = ["mortality"])
        
        new_df = df.style.background_gradient(cmap="PuBu", subset = ["ACS"])\
                    .background_gradient(cmap="YlOrRd", subset = ["ADR"])\
                    .highlight_between(left = avg_acs-5, right = avg_acs+5, subset = ["ACS"], color = "mediumslateblue")\
                    .highlight_between(left = acsie - 2, right = acsie + 2, subset = ["ACS"], color="seagreen")\
                    #.highlight_between(left = adrie - 1, right = adrie + 1, color="cornflowerblue", subset = ["ADR"])
        #to get list of colors can just put a randome comb of letters istead of PuBu
        worksheet.write_string(0,0, namer + " match stats")
        #goes by row then column, starting at 0
        new_df.to_excel(writer, sheet_name = namer, startrow=1, startcol=0)

        new_mort_df = mort_df.style.background_gradient(cmap="seismic", subset=[namer], vmin = mort_rate-.05, vmax = mort_rate+.05)
        new_mort_df.to_excel(writer, sheet_name = namer, startrow = df.shape[0] + 5)


        worksheet.write_string(df.shape[0] + mort_df.shape[0] + 9,0, namer + " map stats")
        df2.to_excel(writer, sheet_name = namer, startrow = df.shape[0] + mort_df.shape[0] + 10)
        #df.shape returns a list of the size of index, column


        worksheet.insert_image(1, df.shape[1] + 3, folder_path + "\\" + namer + ".png", {'x_scale': .5, 'y_scale': .5})
    all_df.to_excel(writer, sheet_name = 'all data')


all_df.plot.scatter(x = 'Total Rounds', y = 'ACS', title = "all data")
ax = plt.gca()
ax.set_xlim([0, 40])
ax.set_ylim([0, 400])

plt.figure()
fig = all_df['ACS'].plot.hist(alpha=0.5, bins = 20, figsize=(10,8), fontsize=(15)).get_figure()
fig.savefig(namer + '.png')


all_df.sort_values(by=['Map', 'ACS'], ascending=False, inplace=True)
#don't forget to use inplace or it will not modify the existing df

test_df = all_df.sort_values(by=['Map', 'ACS'], ascending=False)
#yep, default in inplace=False, which mean it will not modify the current df.
#have to copy the sort_val df to a different df

print(os.getcwd())
print("done with task")


'''for root, dirs, files in os.walk(folder_path):
    for name in files:
        try:
            if name.endswith((".html", ".htm")):
                f = open(name, 'r')
                print(dfer(f.name))
        finally:
            f.close()
            '''
