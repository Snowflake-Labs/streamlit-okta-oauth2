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
from streamlit_okta import okta_login_wrapper


def app():
    # Here came your business logic
    st.header("You are logged in successfully!")


def main():
    okta_config = {
        "okta_base_url": "",
        "client_id": "",
        "client_secret": "",
        "redirect_uri": "",
    }

    okta_login_wrapper(okta_config, app)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.write(e)
        raise e
