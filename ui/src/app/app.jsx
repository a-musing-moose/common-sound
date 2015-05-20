(function () {
    var React = require('react'),
        injectTapEventPlugin = require("react-tap-event-plugin"),
        Main = require('./components/main.jsx');

    //Needed for React Developer Tools
    window.React = React;

    injectTapEventPlugin();

    React.render(<Main />, document.body);

})();
