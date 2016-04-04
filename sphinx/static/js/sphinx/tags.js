$(document).ready(function () {
    var tagResults = ReactDOM.render(
        React.createElement(
            TagResults, {
                source: $('#tag-search'),
                data: $('#tags-data').html(),
                matchCount: $('#match-count')
            }
        ),
        document.getElementById("results-container")
    );

    $('#tag-search').on('input', tagResults.search);
});

var TagResults = React.createClass({
    displayName: "TagResults",
    allTags: null,
    fuse: null,

    fuseOptions: {
        keys: ['name'],
        maxPatternLength: 200,
        tokenize: true
    },

    componentDidMount: function () {
        this.allTags = JSON.parse(this.props.data);
        this.fuse = new Fuse(this.allTags, this.fuseOptions);

        // trigger search
        this.search();
    },

    getInitialState: function () {
        return {
            selectedTags: []
        };
    },

    render: function () {
        return React.createElement(
            "ul", {
                style: {
                    padding: 0,
                    listStyle: "none",
                    marginLeft: -10
                }
            },
            this.state.selectedTags.map(function (tag) {
                return React.createElement(Tag, {name: tag.name});
            })
        );
    },

    componentDidUpdate: function () {
        this.props.matchCount.html(this.state.selectedTags.length + " Tags");
    },

    search: function () {
        // get search term from source
        var input = this.props.source.val();

        if (input === "") {
            this.setState({
                selectedTags: this.allTags
            });
            return;
        }

        // update state with selected tags
        this.setState({
            selectedTags: this.fuse.search(input)
        });
    }
});

var Tag = React.createClass({
    displayName: "Tag",

    render: function () {
        return React.createElement("li", {
            style: {
                padding: 10,
                margin: 10,
                border: "1px solid gray",
                display: "inline-block"
            }
        }, this.props.name);
    }
});