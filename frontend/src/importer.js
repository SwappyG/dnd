import React from 'react';

export class Importer extends React.Component {
    constructor(props) {
        super(props)
    }

    render() {
        return (
            <div class="row">
                <div class="col-2">
                    <h2>Import</h2>
                </div>
                <div class="col-10">
                    <form class="form-inline" action="/importer" method="POST">
                        <div class="form-group mb-2">
                            <div class="custom-file">
                                <input type="file" class="custom-file-input" id="importfile" name="importfile" required />
                                <label class="custom-file-label" for="importfile">Choose file...</label>
                            </div>
                        </div>
                        <div class="form-group mx-sm-3 mb-2">
                            <select class="custom-select" id="type" name="type">
                                <option value="effects">Effects</option>
                                <option value="features">Features</option>
                                <option value="options">Options</option>
                                <option value="jobs">Jobs</option>
                                <option value="items">Items</option>
                            </select>
                        </div>
                        <div class="form-group">
                            <button type="submit" class="btn btn-primary mb-2">Upload</button>
                        </div>
                    </form>
                </div>
            </div>
        );
    }
}