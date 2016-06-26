var OpenExplorerWidget = React.createClass({
    explorerData: null,
    displayName: "OpenExplorerWidget",
    fixedStandard: 1,
    updateFixedStandard: function (newFixedStandard) {
        this.fixedStandard = newFixedStandard;
        this.setState(this.getInitialState());
    },

    getInitialState: function () {
        return {
            selected_subjectroom: 0,
            selected_standard: this.fixedStandard,
            selected_chapter: 0,
            selected_aql: 0
        };
    },

    componentDidMount: function () {
        $.getJSON(AJAX_ENDPOINT + this.props.data_endpoint, function (data) {
            //set data and reload
            this.explorerData = data;
            this.setState(this.getInitialState());
        }.bind(this));
    },

    subjectroomChanged: function () {
        this.setState({
            selected_subjectroom: parseInt(event.target.id),
            selected_standard: this.fixedStandard,
            selected_chapter: 0,
            selected_aql: 0
        });
    },
    // standardChanged: function(event) {
    //     this.setState({
    //         selected_standard: parseInt(event.target.id),
    //         selected_chapter: 0,
    //         selected_aql: 0
    //     });
    // },
    chapterChanged: function (event) {
        this.setState({
            selected_chapter: parseInt(event.target.id),
            selected_aql: 0
        });
    },
    aqlChanged: function (event) {
        this.setState({
            selected_aql: parseInt(event.target.id)
        });
    },
    render: function () {
        //build list of all subjectrooms that are available
        var subjectrooms = [];
        if (this.explorerData != null) {
            subjectrooms = this.explorerData;
        }

        // build list of all standards that are available for the currently selected subjectroom
        var standards = [];
        if (subjectrooms.length > 0) {
            for (var i = 0; i < subjectrooms.length; i++) {
                if (subjectrooms[i].subjectroom_id === this.state.selected_subjectroom) {
                    standards = subjectrooms[i].standards;
                    break;
                }
            }
        }

        // build list of all chapters that are available for the currently selected standard
        var chapters = [];
        if (standards.length > 0) {
            for (var i = 0; i < standards.length; i++) {
                if (standards[i].standard_id === this.state.selected_standard) {
                    chapters = standards[i].chapters;
                    break;
                }
            }
        }

        // build list of all aqls that are available for the currently selected chapter
        var aqls = [];
        if (chapters.length > 0) {
            for (var i = 0; i < chapters.length; i++) {
                if (chapters[i].chapter_id === this.state.selected_chapter) {
                    aqls = chapters[i].aqls;
                    break;
                }
            }
        }

        // look at the currently selected aql and grab the description
        var description = null;
        if (aqls.length > 0) {
            for (var i = 0; i < aqls.length; i++) {
                if (aqls[i].aql_id === this.state.selected_aql) {
                    description = aqls[i].description;
                    break;
                }
            }
        }

        if (this.state.selected_aql > 0) {
            this.props.target.val(this.state.selected_aql);
            if (this.props.aql_selected_callback) {
                this.props.aql_selected_callback(this.state.selected_aql);
            }
        }
        else {
            this.props.target.val("");
            if (this.props.aql_unselected_callback) {
                this.props.aql_unselected_callback();
            }
        }

        return React.createElement("div", null,
            this.buildExplorerTab(
                3,
                "subjectroom",
                "Subject",
                subjectrooms,
                this.state.selected_subjectroom,
                this.subjectroomChanged
            ),
            // this.buildExplorerTab(
            //     1,
            //     "standard",
            //     "Grade",
            //     standards,
            //     this.state.selected_standard,
            //     this.standardChanged
            // ),
            this.buildExplorerTab(
                4,
                "chapter",
                "Chapter",
                chapters,
                this.state.selected_chapter,
                this.chapterChanged
            ),
            this.buildExplorerTab(
                1,
                "aql",
                "Set #",
                aqls,
                this.state.selected_aql,
                this.aqlChanged
            ),
            React.createElement("div", {className: "col-md-4 col-sm-4 col-xs-4 explorer-tab", id: "description-tab"},
                React.createElement("div", {className: "row tab-header"}, "Description"),
                React.createElement("div", {id: "description-holder"}, description)
            )
        );
    },

    buildExplorerTab: function (col_width, tag, heading, data_list, relevant_state, on_click) {
        return React.createElement("div", {
                className: "col-md-" + col_width + " col-sm-" + col_width + " col-xs-" + col_width + " explorer-tab",
                id: tag + "-tab"
            },
            React.createElement("div", {className: "row tab-header"}, heading),
            React.createElement("ul", {className: tag + "-list list-unstyled"},
                data_list.map(function (elem) {
                    var className = null;
                    if (relevant_state == elem[tag + '_id']) {
                        className = "explorer-selected"
                    }
                    return React.createElement("li", {
                        onClick: on_click,
                        className: className,
                        id: elem[tag + '_id']
                    }, elem.label);
                }.bind(this))
            )
        )
    }
});

