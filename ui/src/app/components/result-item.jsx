var React = require('react'),
    mui = require('material-ui'),
    FlatButton = mui.FlatButton;

var ResultItem = React.createClass({
    render: function() {
        return (
            <div className="result-item">
                <FlatButton onClick={this.trackSelected}>
                    <span className="mui-flat-button-label">
                        {this.props.track.name} by {this.props.track.artists[0].name}
                    </span>
                </FlatButton>
            </div>
        );
    },

    trackSelected: function() {
        this.props.enqueue(this.props.track.uri);
    }
});


module.exports = ResultItem;
