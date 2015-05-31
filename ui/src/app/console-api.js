
function registerApi(sound) {
    window.pause = function() {
        sound.pause();
    }
    window.sparkle = function() {
        sound.play("spotify:track:7bwQN3Qk0WcBQdkwHQuTho");
    }
    window.enqueue = function(uri) {
        sound.enqueue(uri);
    }
    window.monkey = function(enabled) {
        sound.monkey(enabled);
    }
}


function printHelp() {
    if (typeof console == "object") {
        var msg = "=============================================================================\n"
                + "  ___  _____  __  __  __  __  _____  _  _    ___  _____  __  __  _  _  ____  \n"
                + " / __)(  _  )(  \\/  )(  \\/  )(  _  )( \\( )  / __)(  _  )(  )(  )( \\( )(  _ \\ \n"
                + "( (__  )(_)(  )    (  )    (  )(_)(  )  (   \\__ \\ )(_)(  )(__)(  )  (  )(_) )\n"
                + " \\___)(_____)(_/\\/\\_)(_/\\/\\_)(_____)(_)\\_)  (___/(_____)(______)(_)\\_)(____/ \n"

                + "\n=============================================================================\n\n"
                + "USAGE:\n"
                + "\tpause() - pause or restart playback\n"
                + "\tenqueue(spotifyTrackUri) - enqueue a track\n"
                + "\tmonkey(enabled) - enable/disable music monkey\n"
                + "\tsparkle() - :WARNING: try at your own risk!";
        console.log(msg);
    }
}


function init(sound) {
    registerApi(sound);
    printHelp();
}


exports.init = init;
