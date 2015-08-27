(function () {

    // Site components
    Site = {

        sidebar_element: document.getElementById("sidebar"),
        container_element: document.getElementById("container"),
        content_element: document.getElementById("content"),
        menu_toggle_element: document.getElementById("menu-toggle"),
        audio_player_object: Player,

        init: function () {

            document.title = "Music Web Player";
            var current_tab = document.getElementById("current");
            if (current_tab) current_tab.id = "";

            /* ---------------------------------------------------------------------------------------------------------
             *  Event handling
             */

            // This function toggles the menu
            var toggle_menu = function () {
                if (Site.sidebar_element.className === "changed-state") {
                    Site.sidebar_element.className = "default-state";
                    Site.container_element.className = "default-state";
                } else {
                    Site.sidebar_element.className = "changed-state";
                    Site.container_element.className = "changed-state";
                }
            };

            // ---------------------------------------------------------------------------------------------------------

            // Load url and call the callback function on its content text
            var load_content = function (url, callback) {
                var xhr = new XMLHttpRequest();

                xhr.onreadystatechange = function () {
                    if (xhr.readyState === 4) {
                        return callback(xhr.responseText);
                    }
                };

                xhr.open('GET', url, true);
                xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
                xhr.send();
            };

            // ---------------------------------------------------------------------------------------------------------

            // Lookup table based on element's node name for the click event
            var click_handlers_by_node_name = {
                "A": function (event) {
                    var target_url = event.target.href;

                    if (target_url !== window.location.href) {
                        load_content(target_url, function (content) {
                            window.history.replaceState({
                                scrollTop: window.scrollY,
                                isMine: true
                            }, "", window.location.href);
                            Site.content_element.innerHTML = content;
                            window.history.pushState("", "", target_url);
                            window.scroll(0, 0);
                        });
                    }

                    event.preventDefault();
                },

                "TD": function (event) {
                    var element = event.target.parentNode;
                    var element_type = element.getAttribute("data-type");
                    var element_id = element.getAttribute("data-id");

                    var target_url = document.createElement("a");
                    target_url.href = "/" + element_type + "s/" + element_id + "/";

                    if (element_type === "track") {
                        Site.audio_player_object.fill_queue(element.parentNode.parentNode); // get the table
                        Site.audio_player_object.start_playing(element.rowIndex);              // row [1..number-of-tracks]
                    } else {
                        load_content(target_url.href, function (content) {
                            window.history.replaceState({
                                scrollTop: window.scrollY,
                                isMine: true
                            }, "", window.location.href);
                            Site.content_element.innerHTML = content;
                            window.history.pushState("", "", target_url.href);
                            window.scroll(0, 0);
                        });
                    }
                }
            };

            // Delegates function based on the element's node name
            var delegate_click_by_node_name = function (event) {
                var target_node_name = event.target.nodeName;

                if (click_handlers_by_node_name[target_node_name]) {
                    click_handlers_by_node_name[target_node_name](event);
                }
            };

            // Add the event listeners

            // Add popstate event listener
            window.addEventListener("popstate", function (event) {
                if (event.state.isMine) {
                    load_content(window.location.href, function (content) {
                        Site.content_element.innerHTML = content;
                        if (event.state.scrollTop) window.scroll(0, event.state.scrollTop);
                    });
                }
            });

            // Add menu toggle click listener
            Site.menu_toggle_element.addEventListener("click", toggle_menu);

            // Add container_element click listener, using bubbling it handles events on its children
            window.addEventListener("click", delegate_click_by_node_name);
        }
    };

    Site.init();

})();
