(function () {
    var s;

    Player = {

        container_element: document.getElementById("player"),
        queue_element: document.getElementById("player-queue"),

        settings: {
            volume: 1.00,
            repeat_playlist: true,
            shuffle: false,
            pre_load: true,
            mime_type: "audio/mpeg"
        },

        //

        fill_queue: function (track_table) {
            if (track_table && track_table.parentNode.id !== "player-queue") {
                Player.clear_queue();
                var track_table_clone = track_table.cloneNode(true);
                Player.queue_element.appendChild(track_table_clone);
                Player.queued_tracks = Player.queue_element.firstChild.rows;
            }
        },

        clear_queue: function () {
            if (Player.queue_element.firstChild) {
                Player.queue_element.removeChild(Player.queue_element.firstChild);
            }
        },

        //

        is_loaded: function () {
            return Player.now_playing_index > 0;
        },

        start_playing: function (row_index) {
            if (row_index < 1 || row_index >= Player.queued_tracks.length) return;

            var requested_track = Player.queued_tracks[row_index];

            Player.player_instance.src = requested_track.getAttribute("data-url");
            Player.player_instance.play();

            var now_playing = document.getElementById("now-playing");
            if (now_playing) now_playing.id = "";
            requested_track.id = "now-playing";

            var track_title = requested_track.cells[1].innerHTML;
            var track_artist = requested_track.cells[2].innerHTML;
            Player.now_playing_artist.innerHTML = track_artist;
            Player.now_playing_title.innerHTML = track_title;
            document.title = "▶ " + track_title + " - " + track_artist;

            var play_button = document.getElementById("player-button-play");
            if (play_button) play_button.id = "player-button-pause";

            var seeker = document.getElementById("seeker");
            seeker.style.width = "0%";

            Player.now_playing_index = row_index;
        },

        pause_playing: function () {
            if (Player.is_loaded() && !Player.player_instance.paused) {
                Player.player_instance.pause();
                document.title = document.title.substring(2);
                document.getElementById("player-button-pause").id = "player-button-play";
            }
        },

        resume_playing: function () {
            if (Player.is_loaded() && Player.player_instance.paused) {
                Player.player_instance.play();
                document.title = "▶ " + document.title;
                document.getElementById("player-button-play").id = "player-button-pause";
            }
        },

        play_next_track: function () {
            if (Player.is_loaded()) Player.start_playing(Player.next_track_index());
        },

        play_previous_track: function () {
            if (Player.is_loaded()) Player.start_playing(Player.previous_track_index());
        },

        //

        random_track_index: function () {
            return Math.floor(Math.random() * (Player.queued_tracks.length - 1)) + 1;
        },

        next_track_index: function () {
            if (Player.settings.shuffle) return Player.random_track_index();

            var index = Player.now_playing_index + 1;
            if (index >= Player.queued_tracks.length && Player.settings.repeat_playlist) index = 1;

            return index;
        },

        previous_track_index: function () {
            if (Player.settings.shuffle) return Player.random_track_index();

            var index = Player.now_playing_index - 1;
            if (index < 1 && Player.settings.repeat_playlist) index = Player.queued_tracks.length - 1;

            return index;
        },

        //

        init: function () {
            s = Player.settings;

            var create_player = function (id) {
                var created_player = document.createElement("audio");
                created_player.setAttribute("id", id);
                created_player.setAttribute("type", s.mime_type);
                created_player.setAttribute("preload", s.pre_load ? "auto" : "none");
                created_player.volume = s.volume;
                Player.container_element.appendChild(created_player);
                return created_player;
            };

            Player.player_instance = create_player("player-instance");

            now_playing_index = -1; // default index indicating that playing hasn't started

            Player.now_playing_title = document.getElementById("playing-track-title");
            Player.now_playing_artist = document.getElementById("playing-track-artist");

            Player.controls_container = document.getElementById("controls");

            // Adding the player event listeners

            window.addEventListener("keydown", function (event) {
                switch (event.keyCode) {
                    case 90: // z -> play_prev_track
                        Player.play_previous_track();
                        break;
                    case 88: // x -> play_next_track
                        Player.play_next_track();
                        break;
                    case 67: // c -> pause, resume track
                        if (Player.player_instance.paused) Player.resume_playing();
                        else Player.pause_playing();
                        break;
                }
            });

            //

            var button_click_handlers = {
                "player-button-previous": Player.play_previous_track,
                "player-button-play": Player.resume_playing,
                "player-button-pause": Player.pause_playing,
                "player-button-next": Player.play_next_track
            };

            Player.controls_container.addEventListener("click", function (event) {
                if (button_click_handlers[event.target.id]) {
                    button_click_handlers[event.target.id]();
                }
            });

            //

            Player.player_instance.addEventListener("timeupdate", function () {
                var seeker = document.getElementById("seeker");
                seeker.style.width = Player.player_instance.currentTime / Player.player_instance.duration * 100 + "%";
            });

            //

            Player.player_instance.addEventListener("ended", function (event) {
                Player.play_next_track();
            });
        }

    };

    Player.init();

})();
