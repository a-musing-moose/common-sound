var React = require('react'),
    mui = require('material-ui'),
    Paper = mui.Paper,
    FlatButton = mui.FlatButton,
    FontIcon = mui.FontIcon;

var Track = React.createClass({
    render: function() {
        var zDepth = 1;
        var className = "track-paper";
        if (this.props.isCurrent) {
            zDepth = 4;
            className += " current";
        }

        var voteButton = null;
        if (this.props.voted === false) {
            voteButton = (
                <span className="button-example-container">
                    <FlatButton onClick={this.vote}>
                        <FontIcon className="fa fa-thumbs-up"/>
                        <span className="mui-flat-button-label">Vote</span>
                    </FlatButton>
                </span>
            );
        }

        return (
            <Paper zDepth={zDepth} className={className}>
                <p>
                    <span className="track-title">
                        {this.props.track.name} by {this.props.track.artists[0].name}
                    </span>
                    {voteButton}
                </p>
            </Paper>
        );
    },

    vote: function() {
        this.props.onVote(this.props.track.uri);
    }
});


module.exports = Track;
