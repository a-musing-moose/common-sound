/** In this file, we create a React component which incorporates components provided by material-ui */

var React = require('react'),
    autobahn = require("autobahn"),
    CommonSound = require('../sound.js'),
    ConsoleApi = require('../console-api.js'),
    mui = require('material-ui'),
    TrackList = require('./track-list.jsx'),
    Search = require('./search.jsx'),
    Todo = require('./todo.jsx'),
    RaisedButton = mui.RaisedButton,
    AppCanvas = mui.AppCanvas,
    Snackbar = mui.Snackbar,
    TextField = mui.TextField;

var Main = React.createClass({

    getInitialState: function() {
        return {
            sound: null,
            track: {"uri": null},
            playlist: [],
            voteUps: [],
            voteDowns: [],
            searchResults: null
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
            var sound = new CommonSound(
                session,
                self.onStatus,
                self.onPlaylist
            );
            self.setState({"sound": sound});

            //provides quick console access if needed
            ConsoleApi.init(sound);

            sound.playlist().then(function(result){
                self.setState({"playlist": result});
            });
        };

        // fired when connection was lost (or could not be established)
        connection.onclose = function (reason, details) {
            if (typeof console == 'object') {
                console.log("Connection lost: " + reason);
            }
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
                            <Search
                                onSearch={this.search}
                                results={this.state.searchResults}
                                clearSearch={this.clearSearch}
                                enqueue={this.enqueue}/>
                            <TrackList tracks={this.state.playlist} current={this.state.track} onVoteUp={this.voteUp} onVoteDown={this.voteDown} votes={this.state.votes} />
                        </div>
                    </div>

                    <div className="full-width-section footer">
                        <p>
                            Hand crafted with love by a-musing-moose and Frankie Boomstick.
                        </p>
                        <Todo />
                    </div>
                </div>
                {currentTrack}
            </AppCanvas>
        );
    },

    search: function(q) {
        var self = this;
        this.state.sound.find(q).then(function(result){
            self.setState({"searchResults": result});
        });
    },

    clearSearch: function() {
        this.setState({"searchResults": null});
    },

    voteUp: function(uri) {
        var self = this;
        var votes = this.state.voteUps;
        votes.push(uri);
        this.state.sound.voteUp(uri).then(function(){
            self.setState({voteUps: votes});
        });
    },

    voteDown: function(uri) {
        var self = this;
        var votes = this.state.voteDowns;
        votes.push(uri);
        this.state.sound.voteDown(uri).then(function(){
            self.setState({voteDowns: votes});
        });
    },

    enqueue: function(uri) {
        this.state.sound.enqueue(uri);
    }

});

module.exports = Main;
