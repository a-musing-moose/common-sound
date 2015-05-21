
function registerApi(sound) {
    window.pause = function() {
        sound.pause();
    }
    window.play = function(uri) {
        sound.play(uri);
    }
    window.sparkle = function() {
        sound.play("spotify:track:7bwQN3Qk0WcBQdkwHQuTho");
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
                + "\tplay(spotifyTrackUri) - play a track immediately\n"
                + "\tsparkle() - :WARNING: try at your own risk!";
        console.log(msg);
    }
}


function init(sound) {
    registerApi(sound);
    printHelp();
}


exports.init = init;
