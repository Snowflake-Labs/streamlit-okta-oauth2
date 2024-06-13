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

import os
from streamlit.components.v1 import html
import streamlit.components.v1 as components

parent_dir = os.path.dirname(os.path.abspath(__file__))
oauth_component_build_dir = os.path.join(parent_dir, "oauth/build")

oauth_component = components.declare_component(
    "oauth_component",
    path=oauth_component_build_dir
)


def onunload_component():
    unload_component_iframe = '''
    <script>
        window.parent.onbeforeunload = (e) => {
            const pTag = Array.from(
                window.parent.document.getElementsByTagName("p"),
            )
                .filter((item) => item.innerHTML === "revoke")
                .shift();
            
            if(pTag){
                pTag.click();
            }
        };   
    </script>
    '''

    html(unload_component_iframe, height=0)
