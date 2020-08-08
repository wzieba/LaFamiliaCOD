import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import styles from './App.css';


function App() {
    return (
        <div className="App">

            <div className="row no-gutters">

                <div className="col-sm-3">
                    <Dimension/>
                </div>
                <div className="col-sm-3">
                    <Dimension/>
                </div>

                <div className="col-sm-3">
                    <Dimension/>
                </div>

                <div className="col-sm-3">
                    <Dimension/>
                </div>
            </div>

        </div>
    );
}

class Dimension extends React.Component {

    render() {
        return (
            <div className={`${styles.card} shadow`}>
                <div className={`card-body`}>
                    <h3 className="card-title text-uppercase">Gracz tygodnia</h3>
                </div>
            </div>
        )
    }
}

export default App;
