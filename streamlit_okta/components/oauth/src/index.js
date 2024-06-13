/* Copyright 2024 Snowflake Inc. 
 SPDX-License-Identifier: Apache-2.0

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.*/

import { Streamlit, RenderData } from "streamlit-component-lib";

let isClicked = false;

const getLocalStorageHandler = (params) => {
    Streamlit.setComponentValue({ ...window.localStorage });
};

const setStateHandler = (params) => {
    localStorage.setItem("state", params.state);
};

const removeStateHandler = (params) => {
    if (localStorage.getItem("state")) {
        localStorage.removeItem("state");
    }
};

const hideRevokeButtonHandler = (params) => {
    const pTag = Array.from(window.parent.document.getElementsByTagName("p"))
        .filter((item) => item.innerHTML === "revoke")
        .shift();

    if (
        pTag &&
        pTag.parentElement &&
        pTag.parentElement.parentElement &&
        pTag.parentElement.parentElement.parentElement
    ) {
        const outerDivElement = pTag.parentElement.parentElement.parentElement;
        outerDivElement.style.display = "none";
    }
};

const event_factory = {
    GET_LOCAL_STORAGE: getLocalStorageHandler,
    SET_STATE: setStateHandler,
    REMOVE_STATE: removeStateHandler,
    HIDE_REVOKE_BUTTON: hideRevokeButtonHandler,
};

function onRender(event) {
    const data = event.detail;

    let app_event = data.args["event"];
    let params = data.args["params"];

    if (!isClicked) {
        event_factory[app_event](params);
        isClicked = true;
    }

    Streamlit.setFrameHeight();
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);

Streamlit.setComponentReady();

Streamlit.setFrameHeight();
