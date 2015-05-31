var React = require('react'),
    mui = require('material-ui'),
    Dialog = mui.Dialog,
    FlatButton = mui.FlatButton,
    FontIcon = mui.FontIcon;


var Todo = React.createClass({
    render: function() {

        var actions = [
            {text: 'Close', ref: "close"},
        ]

        return (
            <div>
                <FlatButton onClick={this.showTodo}>Todo</FlatButton>
                <Dialog
                  ref="todo"
                  title="Still to do"
                  actions={actions}
                  actionFocus="close"
                  modal={true}
                  dismissOnClickAway={true}>
                    <ul>
                        <li>Improve search - add albums and artists</li>
                        <li>Add skip by consensus</li>
                        <li>Add remove by consensus</li>
                        <li>Add playlist persistence</li>
                        <li>Spend some time on the less files and front end tweaks</li>
                        <li>Make this dialog look less crap</li>
                    </ul>
                </Dialog>
            </div>
        );
    },

    showTodo: function() {
        this.refs.todo.show()
    }
});


module.exports = Todo;
