import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

require('./App.css');


function App() {
    return (
        <div className="App">

            <div className="row no-gutters">

                <div className="col">
                    <Dimension title="Gracz tygodnia"/>
                </div>
                <div className="col">
                    <Dimension title="Nawjwięcej ukarał"/>
                </div>

                <div className="col">
                    <Dimension title="Gułager tygodnia"/>
                </div>

                <div className="col">
                    <Dimension title="Najszybszy punkciarz"/>
                </div>
            </div>

        </div>
    );
}

interface DimensionProps {
    title: string;
}

enum PointsHolderColor {
    RED = "red",
    BLUE = "blue",
    YELLOW = "yellow"
}

class Dimension extends React.Component<DimensionProps> {

    render() {
        return (
            <div className="card shadow m-1">
                <div className="card-body">
                    <h3 className="card-title text-uppercase">{this.props.title}</h3>

                    <h4 className="text-center">Username</h4>

                    <div className="row">
                        <PointsHolder value={124} color={PointsHolderColor.BLUE}/>
                        <PointsHolder value={124} color={PointsHolderColor.RED}/>
                        <PointsHolder value={124} color={PointsHolderColor.YELLOW}/>
                    </div>
                </div>
            </div>
        )
    }
}

interface PointsHolderProps {
    value: number
    color: PointsHolderColor
}

class PointsHolder extends React.Component<PointsHolderProps> {

    render() {
        return (
            <div className="col text-center">
                <button className={`btn ${this.props.color.toString()}`}>{this.props.value}</button>
            </div>
        )
    }
}

export default App;
