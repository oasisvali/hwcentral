var ExplorerWidget = React.createClass({
    explorerData: null,
    displayName: "ExplorerWidget",

    getInitialState: function () {
        var selections = [];
        for (var i = 0; i < this.props.panes.length; i++) {
            selections.push(0);
        }

        if (selections.length > 0) {
            if (this.props.first_pane_initial_selection) {
                selections[0] = this.props.first_pane_initial_selection();
            }
        }

        return {
            selections: selections
        };
    },

    componentDidMount: function () {
        $.getJSON(AJAX_ENDPOINT + this.props.data_endpoint, function (data) {
            //set data and reload
            this.explorerData = data;
            this.setState(this.getInitialState());
        }.bind(this));
    },

    selectionChanged: function (paneIndex, selection) {
        var new_selections = [];
        for (var i = 0; i < this.props.panes.length; i++) {
            if (i < paneIndex) {
                new_selections.push(this.state.selections[i]);
            }
            else if (i === paneIndex) {
                new_selections.push(selection);
            }
            else {
                new_selections.push(0);
            }
        }
        this.setState({
            selections: new_selections
        });
    },

    paneChanged: function (paneIndex) {
        this.selectionChanged(paneIndex, parseInt(event.target.id));
    },

    render: function () {
        var root = this.explorerData;
        var paneLists = [];
        for (var i = 0; i < this.props.panes.length; i++) {
            var paneList = [];

            if ((root != null) && (root.length > 0)) {
                if (i === 0) {
                    paneList = JSON.parse(JSON.stringify(root));
                }
                else {
                    for (var j = 0; j < root.length; j++) {
                        if (root[j].id === this.state.selections[i - 1]) {
                            paneList = JSON.parse(JSON.stringify(root[j].child_nodes));
                            break;
                        }
                    }
                }
            }

            root = JSON.parse(JSON.stringify(paneList));

            paneLists.push(paneList);
        }

        // look at the currently selected last pane and grab the description
        var description = null;
        var lastPaneList = paneLists[paneLists.length - 1];
        var lastSelection = this.state.selections[this.state.selections.length - 1];
        if (lastPaneList.length > 0) {
            for (var i = 0; i < lastPaneList.length; i++) {
                if (lastPaneList[i].id === lastSelection) {
                    description = lastPaneList[i].description;
                    break;
                }
            }
        }

        if (lastSelection > 0) {
            this.props.target.val(lastSelection);
            if (this.props.aql_selected_callback) {
                this.props.aql_selected_callback(lastSelection);
            }
        }
        else {
            this.props.target.val("");
            if (this.props.aql_unselected_callback) {
                this.props.aql_unselected_callback();
            }
        }

        return React.createElement("div", null,
            this.props.panes.map(function (o, i) {
                if (i === 0) {
                    if (this.props.skip_first_pane) {
                        return;
                    }
                }
                var pane_title = o[0];
                var pane_width = o[1];
                return this.buildExplorerTab(
                    pane_width,
                    pane_title,
                    paneLists[i],
                    this.state.selections[i],
                    i
                );
            }.bind(this)),
            React.createElement("div", {
                    className: "col-md-" + this.props.description_width + " col-sm-" + this.props.description_width + " col-xs-" + this.props.description_width + " explorer-tab",
                    id: "description-tab"
                },
                React.createElement("div", {className: "row tab-header"}, "Description"),
                React.createElement("div", {id: "description-holder"}, description)
            )
        );


    },

    buildExplorerTab: function (col_width, heading, paneList, selection, paneIndex) {
        return React.createElement("div", {
                className: "col-md-" + col_width + " col-sm-" + col_width + " col-xs-" + col_width + " explorer-tab"
            },
            React.createElement("div", {className: "row tab-header"}, heading),
            React.createElement("ul", {className: "list-unstyled"},
                paneList.map(function (elem) {
                    var className = null;
                    if (selection == elem.id) {
                        className = "explorer-selected"
                    }
                    return React.createElement("li", {
                        onClick: function () {
                            this.paneChanged(paneIndex);
                        }.bind(this),
                        className: className,
                        id: elem.id
                    }, elem.label);
                }.bind(this))
            )
        )
    }
});

