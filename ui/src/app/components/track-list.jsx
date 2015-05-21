var React = require('react'),
    Track = require('./track.jsx');

var TrackList = React.createClass({
    render: function(){

        var tracks = [];
        for (var i=0; i<this.props.tracks.length; i++) {
            var track = this.props.tracks[i];
            var isCurrent = false;
            if (track.uri == this.props.current.uri) {
                isCurrent = true;
            }
            var voted = false;
            if (this.props.votes.indexOf(track.uri) > -1) {
                voted = true;
            }
            tracks.push(
                <li key={track.uri} className="track">
                    <Track track={track} isCurrent={isCurrent} onVote={this.props.onVote} voted={voted} />
                </li>
            );
        }

        return (
            <div className="playlist">
                <h3>Playlist</h3>
                <ul className="track-list">
                    {tracks}
                </ul>
            </div>
        );
    }
});


module.exports = TrackList;
