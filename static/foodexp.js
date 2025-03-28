function predict_foodexp() {
    const salary=document.getElementById("salary").value
    console.log(salary)
    document.getElementById('foodexp').innerText = 
        "Predicted Food Expenditure: " + (salary * 0.48517842 + 147.47538852370565).toFixed(2)
}