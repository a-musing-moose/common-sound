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

        var minutes = ((this.props.track.duration/1000/60) << 0) + "",
            seconds = ((this.props.track.duration/1000) % 60) + "";

        if (seconds.length == 1) {
            seconds = "0" + seconds;
        }
        var duration = minutes + ":" + seconds;



        return (
            <Paper zDepth={zDepth} className={className}>
                <p className="track-content">
                    <span className="track-title">
                        {this.props.track.name} by {this.props.track.artists[0].name}
                        <span className="track-duration mui-font-style-caption">[{duration}]</span>
                    </span>
                    <span className="vote-button">
                    <FlatButton onClick={this.vote} disabled={this.props.voted}>
                        <FontIcon className="fa fa-thumbs-up"/>
                        <span className="mui-flat-button-label">Vote</span>
                    </FlatButton>
                </span>
                </p>
            </Paper>
        );
    },

    vote: function() {
        this.props.onVote(this.props.track.uri);
    }
});


module.exports = Track;
