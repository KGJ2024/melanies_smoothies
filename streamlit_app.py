# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw Customize Your Smoothie :balloon:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

#option = st.selectbox(
#    'What is your favorite fruit ?', ('Banana', 'Strwberries', 'Peaches')
#)
#st.write('Your favorite fruit is:', option)



NAME_AN_ORDER = st.text_input("Name on Smoothie")
st.write("The name of your smoothie will be", NAME_AN_ORDER)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_Name'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect( 
    "Choose upto 5 ingredients"
    , my_dataframe, max_selections = 5
)

if ingredients_list: 
   # st.write("You selected:", ingredients_list)
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += ' ' + fruit_chosen        

    st.write("You selected:", ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_AN_ORDER)
            values ('""" + ingredients_string + """', '""" + NAME_AN_ORDER + """')"""

    
    #st.write(my_insert_stmt)
    #st.stop()

    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
