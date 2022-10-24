# Run config file
execfile('../../config/config_oct2022.py')

# Package specific to grabbing API based data should have been grabbed in config

# FRED API key: 11824d95b466a7d1067e671666863771
fred = Fred('./data/config/fredapi.txt')

fred.get_api_key_file()


fred.get_series_df('JPNPROINDMISMEI')

fred.series_stack
fred.get_child_categories(2)










# Download IMF data
sdmx.list_sources()

imf_flow = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/Dataflow'

json_flow = requests.get(imf_flow).json()
json_flow

df1 = pd.json_normalize(response['Structure']).T
df1

df2 = pd.json_normalize(df1.T['Dataflows.Dataflow'].explode().tolist())
df2

str(df2.iloc[0, 0])

imf_dstructure = 'http://dataservices.imf.org/REST/SDMX_JSON.svc/DataStructure/' + str(df2.iloc[0, 7])
imf_dstructure

json_dstruc = requests.get(imf_dstructure).json()
json_dstruc




 











# FUCK THE PEOPLE AT THE ADB>>>> FUCKING MORONS

adb_code_url = 'https://kidb.adb.org/api/v2/sdmx/data/IMF/A.RAFAGOLDNV_USD.AUS?startPeriod=2010&endPeriod=2020&&output_format=json'

adb_code = requests.get(adb_code_url, verify = False)
adb_code.status_code

adb_code.json()






str(adb_code.content)

with open(str(adb_code.content)) as f:
    df = json.load(f)

pd.read_json(adb_code_url)


adb_code = requests.get(adb_code_url, verify = False)

with open(reqeuests.get)






#########################################################################
# ssl._create_default_https_context = ssl._create_unverified_context
#########################################################################










sdmx.Request('IMF').datastructure()




wbstats = sdmx.Request('WB')






metadata_wb = wbstats.datastructure()

wb_dsd_url = 'http://api.worldbank.org/v2/sdmx/rest/datastructure/wb'
wb_dsd = requests.get(wb_dsd_url, verify = False)

wb_code_url = 'http://api.worldbank.org/v2/sdmx/rest/codelist/wb'
wb_code = requests.get(wb_code_url, verify = False).content

wb.series.info(q = 'manufa')



















# root = ET.XML(wb_code)

def get_feed(url):
    """Scrapes an XML feed from the provided URL and returns XML source.
    
    Args: url (string): Fully qualified URL prointing to XML feed.
    
    Returns: source (string): XML source of scraped feed."""

    try:
        response = urllib.request.urlopen(urllib.request.Request(url, headers = {'User-agent': 'Mozilla'}))
        source = BeautifulSoup(response, 'lxml-xml', from_encoding = response.info().get_param('charset'))
        return source

    except Exception as e:
        print('Error: ' + str(e))

wb_code_xml = get_feed(wb_code_url)

def get_elements(xml, item = 'item'):
    try:
        items = xml.find_all(item)
        elements = [element.name for element in items[0].find_all()]
        return list(set(elements))
    except Exception as e:
        print('Error: ' + str(e))

elements = get_elements(wb_code_xml, item = 'Codelist')
elements

def feed_to_df(url, item = 'item'):
    xml = get_feed(url)
    elements = get_elements(xml, item)

    if isinstance(elements, typing.List):
        df = pd.DataFrame(columns = elements)

        items = xml.find_all(item)

        for item in items:
            row = {}
            for element in elements:
                if xml.find(element):
                    if item.find(element):
                        row[element] = item.findNext(element).text
                    else:
                        row[element] = ''
                else:
                    row[element] = ''

            df = df.append(row, ignore_index = True)
        return df

wb_code_df = feed_to_df(wb_code_url, item = 'Codelist')

wb_code_df

                    




























def parse_XML(xml_file, df_cols): 
    """Parse the input XML file and store the result in a pandas 
    DataFrame with the given columns. 
    
    The first element of df_cols is supposed to be the identifier 
    variable, which is an attribute of each node element in the 
    XML data; other features will be parsed from the text content 
    of each sub-element. 
    """
    
    xtree = ET.parse(xml_file)
    xroot = xtree.getroot()
    rows = []
    
    for node in xroot: 
        res = []
        res.append(node.attrib.get(df_cols[0]))
        for el in df_cols[1:]: 
            if node is not None and node.find(el) is not None:
                res.append(node.find(el).text)
            else: 
                res.append(None)
        rows.append({df_cols[i]: res[i] 
                     for i, _ in enumerate(df_cols)})
    
    out_df = pd.DataFrame(rows, columns=df_cols)
        
    return out_df

parse_XML(wb_code, ['Codelist', 'Code', 'Name'])







pd.read_xml(wb_code)

with open('wb_code.xml', 'wb') as output:
    output.write(wb_code.content)

xml_test = pd.read_xml('wb_code.xml')
xml_test

def iter_docs(author):
    author_attr = author.attrib
    for doc in author.iter('document'):
        doc_dict = author_attr.copy()
        doc_dict.update(doc.attrib)
        doc_dict['data'] = doc.text
        yield doc_dict

xml_data = io.StringIO()

etree = ET.parse(xml_data)
doc_df = pd.DataFrame(list(iter_docs(etree.getroot())))





dls = 'https://kidb.adb.org/api/v2/sdmx/data/IMF/A.RAFAGOLDNV_USD.AUS?startPeriod=2005&endPeriod=2015&&output_format=csv'
dls2 = 'https://kidb.adb.org/api/v2/sdmx/metadata/dataflow/{agency}'
dls3 = 'https://kidb.adb.org/api/v2/sdmx/metadata/codelist'

base_site = 'https://kidb.adb.org/api/v2/sdmx/data/'

# {flowref}
# {sdmx_key}
#   FREQUENCY.INDICATOR_KEY.ECONOMY_CODE(S)
#   To get the list of indicator keys and dimension values, refer to the metadata codelist described 
#   Use ALL as economy code for all economies
# {optionalParameters}
#   startPeriod
#   endPeriod
#   format
#   output_format JSON or CSV




resp = requests.get(dls, verify = False)

test1 = requests.get(dls3, verify = False)

with open('test3.xml', 'wb') as output:
    output.write(test1.content)



with open('test.csv', 'wb') as output:
    output.write(resp.content)

?open

print(output)

output





pd.read_csv('./data/EGEDA/EGEDA_2020_created_14102022.csv')