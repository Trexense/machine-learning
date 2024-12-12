import pandas as pd

labels = ['cheap', 'luxurious', 'clean', 'cozy',
       'good service', 'nice view', 'parking', 'pool', 'spa', 'gym', 'wifi',
       'strategic', 'delicious', 'breakfast', 'safety', 'family', 'pet',
       'aesthetic', 'disability', 'laundry']

def generate_user_score(df_user_clicks, df_user_bookmarked, df_hotel, labels = labels):

  df_merged = pd.merge(df_user_clicks[['id', 'userid', 'hotelid']], 
                        df_user_bookmarked[['userid', 'hotelid', 'id']], 
                        on=['userid', 'hotelid'], 
                        how='outer', 
                        suffixes=('_click', '_book'))
    
  df_merged['isclicked'] = df_merged['id_click'].notna().astype(int)
  df_merged['isbooked'] = df_merged['id_book'].notna().astype(int)

  df_merged = df_merged[['userid', 'hotelid', 'isclicked', 'isbooked']]

  df_merged = df_merged.rename(columns={'userid': 'userid', 
                                        'hotelid': 'hotelid', 
                                        'isclicked': 'isclicked', 
                                        'isbooked': 'isbooked'})
  
  df_merged['activityid'] = df_merged.index + 1 

  df_user_history = df_merged

  df_user_history = pd.merge(df_user_history, df_hotel.drop(['name'], axis = 1), on='hotelid', how='inner')

  # for label in labels:
  #     df_user_history[label] = df_user_history[label] + df_user_history['is_booking'] * 5

  df_user_history = df_user_history.drop(['activityid', 'hotelid','isclicked', 'isbooked'], axis=1)

#   print(df_user_history.info)

  df_user_history = df_user_history.groupby('userid').mean()

  return df_user_history
