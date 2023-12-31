import time
import logging
import streamlit as st
import inspect

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(thread)d %(asctime)s %(levelname)s %(message)s')

logger.info(f'starting cycle with state {st.session_state}')
msg_received = inspect.currentframe().f_back.f_back.f_locals['request']
logger.info(f'because of message received {msg_received}')

st.title('playground')

if 'results' not in st.session_state:
    st.session_state.results = []

tab1, tab2 = st.tabs(['Tab1', 'Tab2'])

with tab1:
    form1 = st.form(key='form1')
    form1.selectbox(
        label='Pick a City',
        options=['Madrid', 'Barcelona', 'Sevilla', 'Valencia', 'Bilbao', 'Zaragoza'],
        key='selected_city'
    )


    def form1_callback():
        logger.info(f'submitting form1 {st.session_state}')
        time.sleep(2)
        st.session_state.results.append(f'{st.session_state.selected_city} has a special color')
        logger.info(f'submitted form1 {st.session_state}')
        st.write(f'form1 submitted: {st.session_state.selected_city}')


    submit_btn = form1.form_submit_button(label='Submit', on_click=form1_callback)
    logger.info(f'submit_btn == {submit_btn}: st.session_state = {st.session_state}')

    st.title('results')
    for result in st.session_state.results:
        st.write(result)
    if not st.session_state.results:
        st.write('no results')


with tab2:
    image_url = st.text_input(
        label='Image URL',
        key='image_url'
    )

    st.file_uploader(
        label='Or Upload your own image',
        key='image_uploader',
        disabled=bool(image_url)
    )

logger.info('cycle finished')
