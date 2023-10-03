import time
import logging
import streamlit as st
import inspect

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(thread)d %(asctime)s %(levelname)s %(message)s')

logger.warning(f'starting cycle with state {st.session_state}')
frame = inspect.currentframe()
while frame and not 'request' in frame.f_locals:
    frame = frame.f_back
if 'request' in frame.f_locals:
    logger.info(f'because of message received {frame.f_locals["request"]}')
else:
    logger.info(f"because of message received -can't show it-")

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


    def form1_submit_cb():
        logger.info(f'submitting form1 {st.session_state}')
        st.session_state.pending_calculations = 4
        logger.info(f'submitted form1 {st.session_state}')
        # st.write(f'form1 submitted: {st.session_state.selected_city}')


    def clear_results_cb():
        st.session_state.results = []
        logger.info(f'cleared results {st.session_state}')


    submit_btn = form1.form_submit_button(label='Submit', on_click=form1_submit_cb)
    logger.info(f'submit_btn == {submit_btn}: st.session_state = {st.session_state}')

    st.button('clear results', on_click=clear_results_cb)

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

# do pending processing
if st.session_state.get('pending_calculations', 0):
    i = st.session_state.pending_calculations
    logger.debug(f'generating result {i}')
    time.sleep(3)
    st.session_state.results.append(f'{st.session_state.selected_city} has a special color {i}')
    st.session_state.pending_calculations -= 1
    logger.info(f'rerunning, pending calculations = {st.session_state.pending_calculations}')
    st.rerun()

logger.warning('cycle finished')
