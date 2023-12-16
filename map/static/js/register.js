const form = document.querySelector("form"),
uField = form.querySelector(".username"),
uInput = uField.querySelector("input"),
pField = form.querySelector(".password"),
pInput = pField.querySelector("input");
cField = form.querySelector(".confirm-password"),
cInput = cField.querySelector("input");
eField = form.querySelector(".email"),
eInput = eField.querySelector("input");

form.onsubmit = (e)=>{
  e.preventDefault(); 
  (uInput.value == "") ? uField.classList.add("shake", "error") : checkUsername();
  (pInput.value == "") ? pField.classList.add("shake", "error") : checkPass();
  (cInput.value == "") ? cField.classList.add("shake", "error") : checkConfirmPass();
  (eInput.value == "") ? eField.classList.add("shake", "error") : checkEmail();

  setTimeout(()=>{ 
    uField.classList.remove("shake");
    pField.classList.remove("shake");
    cField.classList.remove("shake");
    eField.classList.remove("shake");
  }, 500);

  uInput.onkeyup = ()=>{checkUsername();} 
  pInput.onkeyup = ()=>{checkPass();}
  cInput.onkeyup = ()=>{checkConfirmPass();}
  eInput.onkeyup = ()=>{checkEmail();} 

  function checkUsername(){
    if(uInput.value == ""){ 
      uField.classList.add("error");
      uField.classList.remove("valid");
    }else{ 
      uField.classList.remove("error");
      uField.classList.add("valid");
    }
  }

  function checkPass() {
    const result = zxcvbn(pInput.value);
    let errorTxt = pField.querySelector(".error-txt");

    if (pInput.value === "") {
        pField.classList.add("error");
        pField.classList.remove("valid");
        errorTxt.innerText = "Password cannot be blank";
    } else if (result.score < 3) {
        pField.classList.add("error");
        pField.classList.remove("valid");
        if (result.feedback.warning === "") {
          errorTxt.innerText = "Password not long enough";
      } else {
          errorTxt.innerText = result.feedback.warning;
      }
    } else {
        pField.classList.remove("error");
        pField.classList.add("valid");
    }
  }

function checkConfirmPass() {
    let errorTxt = cField.querySelector(".error-txt");

    if (cInput.value === "") {
        cField.classList.add("error");
        cField.classList.remove("valid");
        errorTxt.innerText = "Confirm password cannot be blank";
    } else if (cInput.value !== pInput.value) {
        cField.classList.add("error");
        cField.classList.remove("valid");
        errorTxt.innerText = "Passwords don't match";
    } else {
        cField.classList.remove("error");
        cField.classList.add("valid");
    }
}


  function checkEmail(){ //checkEmail function
    let pattern = /^[^ ]+@[^ ]+\.[a-z]{2,3}$/; //pattern for validate email
    if(!eInput.value.match(pattern)){ //if pattern not matched then add error and remove valid class
      eField.classList.add("error");
      eField.classList.remove("valid");
      let errorTxt = eField.querySelector(".error-txt");
      //if email value is not empty then show please enter valid email else show Email can't be blank
      (eInput.value != "") ? errorTxt.innerText = "Enter a valid email address" : errorTxt.innerText = "Email can't be blank";
    }else{ //if pattern matched then remove error and add valid class
      eField.classList.remove("error");
      eField.classList.add("valid");
    }
  }
  if(!uField.classList.contains("error") && !pField.classList.contains("error") && !eField.classList.contains("error") && !cField.classList.contains("error")){
    form.submit(); 
  }
}