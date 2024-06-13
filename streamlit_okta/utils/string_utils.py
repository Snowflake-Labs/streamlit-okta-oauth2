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

import base64
import os
import re


def generate_random_cryptographic_string():
    crypt_string = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
    crypt_string = re.sub('[^a-zA-Z0-9]+', '', crypt_string)
    return crypt_string
