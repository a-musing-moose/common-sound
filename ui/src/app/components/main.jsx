/** In this file, we create a React component which incorporates components provided by material-ui */

var React = require('react'),
    CommonSound = require('../sound.js');
    mui = require('material-ui'),
    TrackList = require('./track-list.jsx'),
    RaisedButton = mui.RaisedButton,
    AppCanvas = mui.AppCanvas,
    Snackbar = mui.Snackbar,
    TextField = mui.TextField;

var Main = React.createClass({

    getInitialState: function() {
        return {
            sound: null,
            track: {"uri": null},
            playlist: []
        };
    },

    componentDidMount: function() {
        var self = this;
        var wsuri;
        if (document.location.origin == "file://") {
            wsuri = "ws://127.0.0.1:8080/ws";
        } else {
            wsuri = (document.location.protocol === "http:" ? "ws:" : "wss:") + "//" + document.location.host + "/ws";
        }

        var connection = new autobahn.Connection({
            url: wsuri,
            realm: "player"
        });

        // fired when connection is established and session attached
        connection.onopen = function (session, details) {
            console.log("Connected");
            var sound = new CommonSound(
                session,
                self.onStatus,
                self.onPlaylist
            );
            self.setState({"sound": sound});
            sound.playlist().then(function(result){
                self.setState({"playlist": result});
            });
        };

        // fired when connection was lost (or could not be established)
        connection.onclose = function (reason, details) {
            console.log("Connection lost: " + reason);
        }
        connection.open();
    },

    onStatus: function (args) {
        var state = args[0];
        try {
            if (state.state == "playing"){
                if (this.state.track.uri !== state.track.uri) {
                    this.setState({"track": state.track});
                    this.refs.currentTrack.show();
                } else {
                    this.refs.currentTrack.dismiss();
                }
            } else {
                this.refs.currentTrack.dismiss();
                this.setState({"track": {"uri": null}});
            }
        } catch (e) {}
    },

    onPlaylist: function (args) {
        console.log(args[0]);
        this.setState({"playlist": args[0]});
    },

    render: function() {

        var currentTrack = null;
        if (this.state.track.uri !== null) {
            var msg = this.state.track.name + " by " + this.state.track.artists[0].name;
            currentTrack = <Snackbar ref="currentTrack" message={msg} />
        }

        return (
            <AppCanvas>
                <div className="mui-app-content-canvas">
                    <div className="home-page-hero full-width-section">
                        <div className="home-page-hero-content">
                            <div className="tagline">
                                <h1>Common Sound</h1>
                                <h2 className="mui-font-style-headline">
                                    A Web Based Music Controller
                                </h2>
                            </div>
                        </div>
                    </div>

                    <div className="full-width-section home-purpose">
                        <div className="full-width-section-content">
                            <TextField
                                ref="searchbox"
                                className="search-box"
                                hintText="Eyedea & Abilities"
                                floatingLabelText="Search for a track or artist" />
                            <RaisedButton
                                label="Lets Play!"
                                onTouchTap={this.search}
                                linkButton={true} primary={true} />
                            <TrackList tracks={this.state.playlist} current={this.state.track} />
                        </div>
                    </div>

                    <div className="full-width-section footer">
                        <p>
                            Hand crafted with love by A Musing Moose and Frankie Boomstick.
                        </p>
                    </div>
                </div>
                {currentTrack}
            </AppCanvas>
        );
    },

    _onLeftIconButtonTouchTap: function() {
        this.refs.leftNav.toggle();
    },

    search: function() {
        var q = this.refs.searchbox.getValue();
        this.refs.searchbox.clearValue();
        this.state.sound.find(q).then(function(result){
            console.log(result);
        });
    }

});

module.exports = Main;
