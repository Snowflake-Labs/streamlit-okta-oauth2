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

import requests
import jwt
import base64
import streamlit as st
from streamlit.components.v1 import html
import logging


class Okta:
    def __init__(self, okta_config) -> None:
        self.okta_base_url = okta_config['okta_base_url']
        self.client_id = okta_config['client_id']
        self.client_secret = okta_config['client_secret']
        self.redirect_uri = okta_config['redirect_uri']
        self.grant_type = 'authorization_code'
        self.response_type = 'code'
        self.response_mode = 'query'
        self.scope = 'openid+email+profile+offline_access'

        authorization_b64_header = base64.b64encode(
            f'{self.client_id}:{self.client_secret}'.encode('ascii')).decode('ascii')

        self.headers = {
            "Authorization": f"Basic {authorization_b64_header}"
        }

    def login_with_okta_component(self, state):
        OKTA_AUTHORIZE_ENDPOINT = f'''
            {self.okta_base_url}/authorize?
            client_id={self.client_id}&
            redirect_uri={self.redirect_uri}&
            response_mode={self.response_mode}&
            response_type={self.response_type}&
            scope={self.scope}&
            state={state}
            '''

        st.info('Redirecting to Okta...')

        st.markdown(f'''
            <head>
                <meta http-equiv="refresh" content="1; URL={OKTA_AUTHORIZE_ENDPOINT}" />
            </head>
            ''', unsafe_allow_html=True)

        logging.debug("Redirected to okta /authorize endpoint")

    def get_tokens_from_okta(self, code):
        data = {
            'code': code,
            'grant_type': self.grant_type,
            'redirect_uri': self.redirect_uri
        }

        OKTA_TOKEN_ENDPOINT = f"{self.okta_base_url}/token"

        response = requests.post(url=OKTA_TOKEN_ENDPOINT,
                                 data=data, headers=self.headers)

        if "error" in response.json():
            st.warning("Something wrong. Please try to login again..")
            logging.debug("/token call failed")
            st.stop()
        else:
            logging.debug("/token call success")
            st.experimental_set_query_params(**{})
            tokens = response.json()

            return tokens

    def refresh_tokens_from_okta(self, **tokens):
        data = {
            'grant_type': "refresh_token",
            "refresh_token": tokens["refresh_token"]
        }

        # /token endpoint
        OKTA_TOKEN_ENDPOINT = f"{self.okta_base_url}/token"

        response = requests.post(url=OKTA_TOKEN_ENDPOINT,
                                 data=data, headers=self.headers)

        if "error" in response.json():
            logging.debug(
                "/token call failed to refresh access and refresh token")
            st.warning("Something wrong. Please try to login again..")
            st.stop()
        else:
            logging.debug(
                "/token call success to refresh access and refresh token")
            new_tokens = response.json()

            st.session_state['token'] = new_tokens

            hide_empty_blocks_html = f'''<script>
                const iframeElements = window.parent.document.getElementsByTagName('iframe');
                Array.from(iframeElements)
                .filter(item=>item.title==='components.oauth_component')
                .forEach(item=>item.parentElement.style.display="none");
            </script>
            '''
            html(hide_empty_blocks_html, height=0)

    def verify_tokens_from_okta(self, **tokens):
        # /introspect endpoint
        OKTA_INTROSPECT_ENDPOINT = f"{self.okta_base_url}/introspect"

        access_token_introspect_data = {
            "token": tokens["access_token"],
            "token_type_hint": "access_token",
        }

        access_token_introspect_response = requests.post(url=OKTA_INTROSPECT_ENDPOINT,
                                                         data=access_token_introspect_data, headers=self.headers)

        refresh_token_introspect_data = {
            "token": tokens["refresh_token"],
            "token_type_hint": "refresh_token",
        }

        refresh_token_introspect_response = requests.post(url=OKTA_INTROSPECT_ENDPOINT,
                                                          data=refresh_token_introspect_data, headers=self.headers)

        if "error" in access_token_introspect_response.json() or "error" in refresh_token_introspect_response.json():
            logging.debug("/introspect failed")
            st.warning("Something wrong. Please try to login again..")
            st.stop()
        else:
            logging.debug(
                "/introspect call success for access and refresh token")

            access_token_introspect_response_data = access_token_introspect_response.json()
            if access_token_introspect_response_data["active"] == False:
                logging.debug("active token expired")

                refresh_token_introspect_response_data = refresh_token_introspect_response.json()
                if refresh_token_introspect_response_data["active"] == True:
                    self.refresh_tokens_from_okta(
                        refresh_token=tokens["refresh_token"])
                elif refresh_token_introspect_response_data["active"] == False:
                    logging.debug("refresh token expired")

                    if 'token' in st.session_state:
                        del st.session_state['token']

                    logging.debug(
                        f"Deleted tokens from Session State and redirecting to {self.redirect_uri}")

                    st.markdown(f'''
                    <head>
                        <meta http-equiv="refresh" content="1; URL={self.redirect_uri}" />
                    </head>
                    ''', unsafe_allow_html=True)

                    st.stop()

    def invalidate_token_from_okta(self, **tokens):
        OKTA_REVOKE_ENDPOINT = f"{self.okta_base_url}/revoke"

        access_token_revoke_data = {
            'token': tokens["access_token"],
            'token_type_hint': "access_token"
        }

        requests.post(url=OKTA_REVOKE_ENDPOINT,
                      data=access_token_revoke_data, headers=self.headers)

        refresh_token_revoke_data = {
            'token': tokens["refresh_token"],
            'token_type_hint': "refresh_token"
        }

        requests.post(url=OKTA_REVOKE_ENDPOINT,
                      data=refresh_token_revoke_data, headers=self.headers)

        if 'token' in st.session_state:
            del st.session_state['token']

    def get_user_context(self):
        if 'token' in st.session_state:
            user_context = jwt.decode(st.session_state['token']['access_token'], options={
                "verify_signature": False})

            return user_context

        return None
