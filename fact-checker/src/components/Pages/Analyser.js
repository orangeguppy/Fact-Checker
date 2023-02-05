import React, { useState } from 'react';
import { 
  MDBTextArea,
  MDBCard,
  MDBCardBody,
  MDBCardTitle,
  MDBCardText,
  MDBBtn,
  MDBContainer
} from 'mdb-react-ui-kit';
import './Analyser.css'

function Analyser() {
  const [inputToCheck, setInput] = useState('Empty String');

  const handleSubmit = (event) => {
    fetch('http://127.0.0.1:5000/verification', {
      method: 'POST',
      body: JSON.stringify({
        'sentence': inputToCheck
      }),
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      },
    })
    .then(response => response.json())
    .then(data => console.log(data));
  }

  return (
    <MDBContainer>
      <MDBCard className='box'>
        <MDBCardBody>
          <MDBCardTitle>What does this thing do and how does it work?</MDBCardTitle>
          <MDBCardText>
            1. Copy and paste the text you want to check into the space below!
            <br />
            2. This tool will sieve out the key points of the text, then determine how likely they are to be false.
            <br />
            3. These potentially false statements will be shown in the area below this box, with relevant links for you to explore.
          </MDBCardText>
          <form onSubmit={(e) => {handleSubmit(e)}}>
            <MDBTextArea label='Enter the input you want to fact-check!' id='textAreaExample' rows={4} onChange={event => setInput(event.target.value)}/>
            <MDBBtn type='submit' block style={{ marginTop:10 }}>
              Verify
            </MDBBtn>
          </form>
        </MDBCardBody>
      </MDBCard>
    </MDBContainer>
  );
}
export default Analyser