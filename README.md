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

# Streamlit Okta OAuth2.0 Authorization Code Flow
This is an okta authentication wrapper library to implement oauth2.0 authentication & authorization in your streamlit application.

## Pre-requisites
- Install following python libraries
  - [streamlit v1.19.0](https://docs.streamlit.io/library/get-started/installation)
  - [requests ](https://anaconda.org/anaconda/requests)  
  - [pyjwt v2.4.0](https://anaconda.org/conda-forge/pyjwt)
- Install node + npm, to build the _custom component_
- Build the _custom component_
 ```
cd streamlit_okta/components/oauth
npm install 
npm run build
```
- Register Client Application in your Okta
    Before you can implement authorization, you need to register your app in Okta by creating an app integration from the Admin Console.
    - In the Admin Console, go to Applications > Applications.
    - Click Create App Integration.
    - Select OIDC - OpenID Connect as the Sign-in method.
    - Select Web Application as the Application type, then click Next.
    - Specify the App integration name.
    - Specify the Sign-in redirect URIs to redirect the user with their authorization code.
    - Fill in the remaining details for your app integration, then click Save.
    
    From the General tab of your app integration, save the generated Client ID and Client secret values to implement your authorization flow.


## Getting started
- Clone the repository
```
git clone <git_repo_url>
```
- Move _streamlit_okta_ folder to your project directory
- Import _okta_login_wrapper_ function into your code
```python
from streamlit_okta import okta_login_wrapper

okta_config = {
        "okta_base_url": "",
        "client_id": "",
        "client_secret": "",
        "redirect_uri": "",
}

'''
Parameters: 
1. okta_config (dict)
    okta_base_url - okta domain url (ex. - https://snowbiz.oktapreview.com/oauth2/v1)
    redirect_uri - redirect url mentioned in okta configuration. It is same as streamlit url (in case of local machine - http://localhost:8501)

2. app (callback function) - contains application business logic
''' 
okta_login_wrapper(okta_config, app)
```

## Example
Refer  [example.py](<git_repo_url>/blob/main/example.py) 
=======
# streamlit-okta-oauth2
