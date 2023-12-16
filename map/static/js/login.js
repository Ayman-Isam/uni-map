// Desc: Javascript for login page
const form = document.querySelector("form"),
uField = form.querySelector(".username"),
uInput = uField.querySelector("input"),
pField = form.querySelector(".password"),
pInput = pField.querySelector("input");

form.onsubmit = (e)=>{
  e.preventDefault(); 
  (uInput.value == "") ? uField.classList.add("shake", "error") : checkUsername();
  (pInput.value == "") ? pField.classList.add("shake", "error") : checkPass();

  setTimeout(()=>{ 
    uField.classList.remove("shake");
    pField.classList.remove("shake");
  }, 500);

  uInput.onkeyup = ()=>{checkUsername();} 
  pInput.onkeyup = ()=>{checkPass();}
  function checkUsername(){
    if(uInput.value == ""){ 
      uField.classList.add("error");
      uField.classList.remove("valid");
    }else{ 
      uField.classList.remove("error");
      uField.classList.add("valid");
    }
  }

  function checkPass(){ 
    if(pInput.value == ""){ 
      pField.classList.add("error");
      pField.classList.remove("valid");
    }else{ 
      pField.classList.remove("error");
      pField.classList.add("valid");
    }
  }

  if(!uField.classList.contains("error") && !pField.classList.contains("error")){
    form.submit(); 
  }
}