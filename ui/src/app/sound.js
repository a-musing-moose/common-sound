/*jslint browser:true */
var soundId = require('./id.js');


CommonSound = function(session, onStatus, onPlaylist) {

    this._session = session;
    this._uri_prefixes = {
        "track": "spotify:track",
        "album": "spotify:album",
        "artist": "spotify:artist",
        "image": "spotify:image"
    }

    this.session = function() {
        if (this._session === null) {
            throw "no session";
        }
        return session;
    }

    this.validate_uri = function(type, uri) {
        var prefix = this._uri_prefixes[type];
        if (false === uri.startsWith(prefix)) {
            throw "invalid " + type + " uri";
        }
    }

    this.find = function(query) {
        var session = this.session();
        return session.call("sound.find", [query])
    }

    this.play = function(uri) {
        this.validate_uri("track", uri);
        var session = this.session();
        return session.call("sound.play", [uri]);
    }

    this.pause = function() {
        var session = this.session();
        return session.call("sound.pause", []);
    }

    this.cover_image = function(uri) {
        this.validate_uri("image", uri);
        session = this.session();
        return session.call("sound.cover_image", [uri]);
    }

    this.enqueue = function(uri) {
        this.validate_uri("track", uri);
        session = this.session();
        return session.call("sound.enqueue", [uri, soundId])
    }

    this.playlist = function() {
        session = this.session();
        return session.call("sound.playlist");
    }

    this.voteUp = function(uri) {
        session = this.session();
        return session.call("sound.vote_up", [uri, soundId]);
    }

    this.voteDown = function(uri) {
        session = this.session();
        return session.call("sound.vote_down", [uri, soundId]);
    }

    this.monkey = function(enabled) {
        if (enabled) {
            return session.call("monkey.enable")
        } else {
            return session.call("monkey.disable")
        }
    }

    session.subscribe('sound.status', onStatus);
    session.subscribe('sound.new_playlist', onPlaylist);
    session.subscribe('sound.force_refresh', function(){
        location.reload();
    });

}

module.exports = CommonSound;
