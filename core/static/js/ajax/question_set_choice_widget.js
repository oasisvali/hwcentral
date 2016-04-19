var ExplorerWidget = React.createClass({
    explorerData: null,
    displayName: "ExplorerWidget",
    getInitialState: function () {
        return {
            selected_subjectroom: 0,
            selected_chapter: 0,
            selected_number: 0
        };
    },

    componentDidMount: function () {
        $.getJSON(AJAX_ENDPOINT + this.props.data_endpoint, function (data) {
            //set data and reload
            this.explorerData = data;
            this.subjectroomChanged();

        }.bind(this));
    },

    subjectroomChanged: function () {
        // check which subjectroom is selected
        var selected_subjectroom = $("#id_subjectroom").val();
        if (selected_subjectroom === "") {
            selected_subjectroom = 0;
        }
        else {
            selected_subjectroom = parseInt(selected_subjectroom);
        }
        this.setState({
            selected_subjectroom: selected_subjectroom,
            selected_chapter: 0,
            selected_number: 0
        });
    },
    chapterChanged: function (event) {
        this.setState({
            selected_chapter: parseInt(event.target.id),
            selected_number: 0
        });
    },
    numberChanged: function (event) {
        this.setState({
            selected_number: parseInt(event.target.id)
        });
    },
    render: function () {
        // build list of all chapters that are available for the currently selected subjectroom by looking at explorerData
        var chapters = [];
        if (this.explorerData != null) {
            for (var i = 0; i < this.explorerData.length; i++) {
                if (this.explorerData[i].subjectroom_id === this.state.selected_subjectroom) {
                    chapters = this.explorerData[i].chapters;
                    break;
                }
            }
        }

        // look at currently selected chapter and build a list of all numbers that are available
        var numbers = [];
        if (chapters.length > 0) {
            for (var i = 0; i < chapters.length; i++) {
                if (chapters[i].chapter_id === this.state.selected_chapter) {
                    numbers = chapters[i].aqls;
                    break;
                }
            }
        }

        // look at the currently selected aql number and grab the description
        var description = null;
        if (numbers.length > 0) {
            for (var i = 0; i < numbers.length; i++) {
                if (numbers[i].aql_id === this.state.selected_number) {
                    description = numbers[i].description;
                    break;
                }
            }
        }

        if (this.state.selected_number > 0) {
            this.props.target.val(this.state.selected_number);
            if (this.props.aql_selected_callback) {
                this.props.aql_selected_callback(this.state.selected_number);
            }
        }
        else {
            this.props.target.val("");
            if (this.props.aql_unselected_callback) {
                this.props.aql_unselected_callback();
            }
        }

        return React.createElement("div", null,
            React.createElement("div", {className: "col-md-4 col-sm-4 col-xs-4 explorer-tab", id: "chapter-tab"},
                React.createElement("div", {className: "row tab-header"}, "Chapter"),
                React.createElement("ul", {className: "chapter-list list-unstyled"},
                    chapters.map(function (chapter) {
                        var className = null;
                        if (this.state.selected_chapter == chapter.chapter_id) {
                            className = "explorer-selected"
                        }
                        return React.createElement("li", {
                            onClick: this.chapterChanged,
                            className: className,
                            id: chapter.chapter_id
                        }, chapter.label);
                    }.bind(this))
                )
            ),
            React.createElement("div", {className: "col-md-2 col-sm-2 col-xs-2 explorer-tab", id: "number-tab"},
                React.createElement("div", {className: "row tab-header"}, "Set #"),
                React.createElement("ul", {className: "number-list list-unstyled"},
                    numbers.map(function (number) {
                        var className = null;
                        if (this.state.selected_number == number.aql_id) {
                            className = "explorer-selected"
                        }
                        return React.createElement("li", {
                            onClick: this.numberChanged,
                            className: className,
                            id: number.aql_id
                        }, number.label);
                    }.bind(this))
                )
            ),
            React.createElement("div", {className: "col-md-6 col-sm-6 col-xs-6 explorer-tab", id: "description-tab"},
                React.createElement("div", {className: "row tab-header"}, "Description"),
                React.createElement("div", {id: "description-holder"}, description)
            )
        );
    }
});

