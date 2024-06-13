# Copyright 2024 Snowflake Inc. 
# SPDX-License-Identifier: Apache-2.0

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit_okta.utils import string_utils
from streamlit.components.v1 import html
from streamlit_okta.components import onunload_component, oauth_component
from streamlit_okta.auth.okta import Okta
import time
import logging


def app(okta, tokens, callback):
    # clean out the query parameters
    st.experimental_set_query_params(**{})
    oauth_component(event='REMOVE_STATE')

    decoded_token = okta.get_user_context()

    # expiry epoch time in UTC
    exp_time = float(decoded_token['exp'])

    # current epoch time in UTC
    current_time = time.time()

    diff = (exp_time - current_time)
    if diff < 0:
        okta.verify_tokens_from_okta(
            access_token=tokens['access_token'], refresh_token=tokens['refresh_token'])

    # Browser / Tab Close Event
    st.button("revoke", on_click=okta.invalidate_token_from_okta,
              kwargs=st.session_state['token'])
    oauth_component(event='HIDE_REVOKE_BUTTON')

    callback()

    # Hide empty blocks
    hide_empty_blocks_html = '''<script>
            const iframeElements = window.parent.document.getElementsByTagName('iframe');

            Array.from(iframeElements)
            .filter(item=>item.title==='st.iframe')
            .forEach(item=>item.parentElement.style.display="none");

            Array.from(iframeElements)
            .filter(item=>item.title==='streamlit_okta.components.oauth_component')
            .forEach(item=>item.parentElement.style.display="none");

            const markdownElement = window.parent.document.getElementsByClassName('stMarkdown');
            Array.from(markdownElement)
            .forEach(item=>item.parentElement.style.display="block");
        </script>
        '''
    html(hide_empty_blocks_html, height=0)


def okta_login_wrapper(config, callback):
    okta = Okta(config)

    onunload_component()
    if 'token' not in st.session_state:
        local_storage = oauth_component(event='GET_LOCAL_STORAGE')
        if local_storage:
            if 'error' in st.experimental_get_query_params():
                st.warning(st.experimental_get_query_params()
                           ['error_description'][0])
                st.stop()

            if "code" in st.experimental_get_query_params() and "state" in st.experimental_get_query_params():
                st.info('Please Wait...')
                authorization_code = st.experimental_get_query_params()[
                    "code"][0]

                authorization_state = st.experimental_get_query_params()[
                    "state"][0]

                if 'state' in local_storage and authorization_state == local_storage['state']:
                    tokens = okta.get_tokens_from_okta(authorization_code)

                    st.session_state['token'] = tokens
                    st.experimental_rerun()
                else:
                    st.warning(
                        "Something wrong. Please try to login again..")
                    st.stop()
            else:
                state = string_utils.generate_random_cryptographic_string()
                oauth_component(event='SET_STATE', params={'state': state})
                okta.login_with_okta_component(state)
                st.stop()
    else:
        logging.debug('User logged in successfully!')
        app(okta, st.session_state['token'], callback)
