var React = require('react'),
    mui = require('material-ui'),
    Paper = mui.Paper;

var Track = React.createClass({
    render: function() {
        var zDepth = 1;
        var className = "";
        if (this.props.isCurrent) {
            zDepth = 4;
            className = "current";
        }
        return (
            <Paper zDepth={zDepth} className={className}>
                <p className="track-title">
                    {this.props.track.name} by {this.props.track.artists[0].name}
                </p>
            </Paper>
        );
    }
});


module.exports = Track;
