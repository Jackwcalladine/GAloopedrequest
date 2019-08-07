#get a list of client accounts in your account
profiles = analytics.management().profiles().list(accountId='12345',
                                                  webPropertyId='~all'
                                                 ).execute()

#looping through json output to get a list of view ID's, assuming you have a json of client accounts
dfnames = []
dfinfo = []
dfid = []
new =[]
for item in data['items']:
    name = item.get('name')
    if name:
        new.append(name)
        webprop = item.get('webProperties')
        if webprop:
            for profile in webprop:
                profile = profile.get('profiles')
                if profile:
                    for idname in profile:
                        idname = idname.get('name')
                    for idname1 in profile:
                        idname1 = idname1.get('id')
                    if idname:
                        result = [idname, idname1]
                    new.append(result)
                else:
                    continue
        else:
            continue

# collect data
keys_list = []
values_list = [[] for _ in range(400)]
count = -1
for item in new:
    if isinstance(item, str):
        keys_list.append(item)
        count += 1
    else:
        values_list[count].append(item)

# create data dictionary
data_dict = dict(zip(keys_list, values_list))
# create data frame
new1 = pd.DataFrame(columns=['Client_name', 'data'])
for key, values in data_dict.items():
    for value in values:
        new1 = new1.append({'Client_name': key, 'data': value}, ignore_index=True)

# split list data into 2 columns
spilt_data = pd.DataFrame(new1['data'].values.tolist(), columns=['dataname','ID'])
# concat data
result = pd.concat([new1, spilt_data], axis=1, sort=False)
# drop used column
result = result.drop(['data'], axis=1)


# making a filtered list that can run through the sample request
df_results = list()

for n in range(0, 5):
    try:
        for i in view_id:
            sample_request = {
                'viewId': 'ga:' + i,
                'dateRanges': {
                    'startDate': '2014-02-01',
                    'endDate': '2019-06-30'
                },
                'dimensions': [{'name': 'ga:medium'}, {'name': 'ga:yearMonth'}, { "name": "ga:segment" }],
                'metrics': [{'expression': 'ga:sessions'}],
                'segments': [{'segmentId': 'gaid::-5'}],
            }
            response = api_client.reports().batchGet(
                body={
                    'reportRequests': sample_request
                }).execute()

            response_data = response.get('reports', [])[0]
            df_results.append((parse_response_single(response_data)[0]))
            print(i)

    except HttpError as error:
        if error.resp.reason in ['userRateLimitExceeded', 'quotaExceeded','internalServerError', 'backendError']:
            time.sleep((2 ** n) + random.random())
    else:
        break
        print("error")

#this returns a dataframe that joins the results from the above API call into a wide data format.
new_df1 = pd.DataFrame()
for i in df_results:
    new_df = i
    new_df1 = pd.concat([new_df, new_df1], axis = 1)
