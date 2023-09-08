import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import seaborn as sns


col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown("Do Visit @: ")
with col2:
    st.markdown(
        "[Linkedin](https://www.linkedin.com/in/prabhat-kumar-prajapati/)")
with col3:
    st.markdown("[Github](https://github.com/PrabhatPrajapati)")
with col4:
    st.markdown("[leetcode](https://leetcode.com/prabhat1999/)")

st.title("WhatsApp Chat Processor")
st.header("Messages in your chat group, `says something?`...Let's find out")
st.subheader("**♟ General Statistics ♟**")
st.write('''* This app is meant as a playground to explore the whatsApp Chat.
    Try it out by `Uploading WITHOUT MEDIA whatsapp chat export` here.''')


st.sidebar.title("Whatsapp Chat Analyzer")

st.sidebar.caption(
    'This application lets you analyze Whatsapp conversations in a very comprehensive manner, with charts, metrics, '
    'and other forms of analysis.')


uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    if len(user_list) >= 3:
        user_list.remove('group_notification')

    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):

        st.title("Chat Dataframe")
        st.dataframe(df)

        data_as_csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=data_as_csv,
            file_name='chat.csv',
            mime='text/csv',
            help="Download the formatted chat as a CSV file",
        )

        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(
            selected_user, df)
        st.header("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.subheader("Total Messages")
            st.subheader(num_messages)
        with col2:
            st.subheader("Total Words")
            st.subheader(words)
        with col3:
            st.subheader("Media Shared")
            st.subheader(num_media_messages)
        with col4:
            st.subheader("Links Shared")
            st.subheader(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],
                daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # activity map
        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most busy day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most busy month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)

        # finding the busiest users in the group(Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)

        # WordCloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # most common words
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax = plt.subplots()

        ax.barh(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')

        st.title('Most commmon words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df = helper.emoji_helper(selected_user, df)
        st.title("Emoji Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax = plt.subplots()
            ax.pie(emoji_df[1].head(),
                   labels=emoji_df[0].head(), autopct="%0.2f")
            st.pyplot(fig)
