# import re
# import pandas as pd


# def preprocess(data):
#     pattern = "\d{1,2}\/\d{1,2}\/\d{2},\s\d{1,2}:\d{2}\s(?:am|pm)\s-\s"

#     messages = re.split(pattern, data)[1:]
#     dates = re.findall(pattern, data)

#     df = pd.DataFrame({'user_message': messages, 'message_date': dates})
#     # convert message_date type
#     df['message_date'] = pd.to_datetime(
#         df['message_date'], format="%d/%m/%y, %I:%M %p - ")

#     df.rename(columns={'message_date': 'date'}, inplace=True)

#     users = []
#     messages = []
#     for message in df['user_message']:
#         entry = re.split('([\w\W]+?):\s', message)
#         if entry[1:]:  # user name
#             users.append(entry[1])
#             messages.append(" ".join(entry[2:]))
#         else:
#             users.append('group_notification')
#             messages.append(entry[0])

#     df['user'] = users
#     df['message'] = messages
#     df.drop(columns=['user_message'], inplace=True)

#     df['only_date'] = df['date'].dt.date
#     df['year'] = df['date'].dt.year
#     df['month_num'] = df['date'].dt.month
#     df['month'] = df['date'].dt.month_name()
#     df['day'] = df['date'].dt.day
#     df['day_name'] = df['date'].dt.day_name()
#     df['hour'] = df['date'].dt.hour
#     df['minute'] = df['date'].dt.minute

#     period = []
#     for hour in df[['day_name', 'hour']]['hour']:
#         if hour == 23:
#             period.append(str(hour) + "-" + str('00'))
#         elif hour == 0:
#             period.append(str('00') + "-" + str(hour + 1))
#         else:
#             period.append(str(hour) + "-" + str(hour + 1))

#     df['period'] = period

#     return df
import re
import pandas as pd

def preprocess(data):
    # Fix 1: Replace narrow no-break space (U+202F) with normal space
    data = data.replace('\u202f', ' ')
    
    # Fix 2: Updated regex pattern for correct date format
    pattern = r"\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2} [APMapm]{2} - "

    # Split data
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Fix 3: Correct date parsing (Month/Day/Year)
    df['message_date'] = pd.to_datetime(
        df['message_date'], format="%m/%d/%y, %I:%M %p - "
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Extract users and messages
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user message
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:  # system message
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add date/time components
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create period column
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")
    df['period'] = period

    return df
