import React from 'react';
import { MDBCard, MDBCardBody, MDBCardText } from 'mdb-react-ui-kit';

function Result(props) {
    let inputStyle = {
        backgroundColor: "#DC4C64",
    };

    if (props.is_rumour === "an unverified rumour") {
        inputStyle = {
            backgroundColor: "#E4A11B",
        }
    }
    return (
        <MDBCard className='box' style={inputStyle}>
            <MDBCardBody>
                <MDBCardText style={{color: "#332D2D"}}>
                    <span style={{ color: 'white' }}>{props.sentence}</span>
                    <br />
                    <span style={{ fontWeight: 'bold' }}>Category:</span>
                    <span style={{ color: 'white' }}> {props.is_rumour}</span>
                </MDBCardText>
            </MDBCardBody>
        </MDBCard>
    )
}
export default Result