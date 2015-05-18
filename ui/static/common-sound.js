/*jslint browser:true */

CommonSound = function(session, listener) {

    this._session = session;

    this.session = function() {
        if (this._session === null) {
            throw new Exception("no session");
        }
        return session;
    }

    this.find = function(query) {
        var session = this.session();
        return session.call("sound.find", [query])
    }

    this.play = function(uri) {
        var session = this.session();
        return session.call("sound.play", [uri]);
    }

    this.pause = function() {
        var session = this.session();
        return session.call("sound.pause", []);
    }

    this.cover_image = function(uri) {
        session = this.session();
        return session.call("sound.cover_image", [uri]);
    }

    this.enqueue = function(uri) {
        session = this.session();
        return session.call("sound.enqueue", [uri])
    }

    this.addStatusListener = function(callback) {
        this.state_listeners.push(callback);
    }

    session.subscribe('sound.status', listener);

}
