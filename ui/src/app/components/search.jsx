var React = require('react'),
    ResultItem = require("./result-item.jsx"),
    mui = require('material-ui'),
    Paper = mui.Paper,
    RaisedButton = mui.RaisedButton,
    FlatButton = mui.FlatButton,
    TextField = mui.TextField,
    FontIcon = mui.FontIcon;

var Search = React.createClass({
    render: function() {

        var tracks = [];
        if (this.props.results !== null) {
            for (var i=0; i<this.props.results.tracks.length; i++) {
                var track = this.props.results.tracks[i];
                tracks.push(
                    <ResultItem key={track.uri} track={track} enqueue={this.enqueue} />
                );
            }
            if (tracks.length <= 0) {
                tracks.push(
                <div key="no-results" className="mui-font-style-display-1">
                    I ain&quot;t found shit.
                </div>
                );
            }
            tracks.push(
                <div key="close-button" className="result-item close-button">
                    <FlatButton onClick={this.props.clearSearch}>
                        <FontIcon className="fa fa-times-circle"/>
                        <span className="mui-flat-button-label">
                            Close
                        </span>
                    </FlatButton>
                </div>
            );
        }

        return (
            <div className="search">
                <form className="commentForm" onSubmit={this.search}>
                    <TextField
                        ref="searchbox"
                        className="search-box"
                        hintText="Eyedea & Abilities"
                        floatingLabelText="Search for a track or artist" />
                    <RaisedButton
                        label="Lets Play!"
                        onTouchTap={this.search}
                        linkButton={true} primary={true} />
                </form>
                <Paper>
                    {tracks}
                </Paper>
            </div>
        );
    },


    search: function(e) {
        e.preventDefault();
        var q = this.refs.searchbox.getValue();
        this.refs.searchbox.clearValue();
        this.props.onSearch(q);
    },

    enqueue: function(uri) {
        this.props.enqueue(uri);
        this.props.clearSearch();
    }
});


module.exports = Search;
