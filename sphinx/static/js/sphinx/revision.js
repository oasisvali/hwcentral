$(document).ready(function () {
    var revisionPreview = ReactDOM.render(React.createElement(RevisionPreview, {source: $('#revision-raw')}), document.getElementById("revision-preview"));
    $('#preview-button').click(revisionPreview.preview);
    $('#format-button').click(revisionPreview.format);
});

var RevisionPreview = React.createClass({
    previewData: null,
    displayName: "RevisionPreview",

    sanitize: function (value) {
        return value
            .trim()
            .replace(/(\r\n|\n|\r)/gm, "")
            .replace(/"/gm, "'")
            .replace(/([^\\])\\([^\\])/gm, "$1\\\\$2");
    },

    getInitialState: function () {
        return {
            revision: this.props.source.val()
        };
    },
    render: function () {
        return React.createElement("div", {
            dangerouslySetInnerHTML: {
                __html: this.state.revision
            }
        });
    },

    componentDidUpdate: function () {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    },

    preview: function () {
        this.setState({
            revision: this.props.source.val()
        });
    },
    format: function () {
        this.props.source.val(this.sanitize(this.props.source.val()));
    }
});