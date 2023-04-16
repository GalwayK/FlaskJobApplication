"use strict";

function addAndDisplayRole(event)
{
    event.preventDefault();
    const strRole = selectRoles.value;
    setRoles.add(strRole);
    const arrRoles = Array.from(setRoles);
    displayRoles(arrRoles);
    inputHidden.value = arrRoles;
    console.log(setRoles);
    console.log(arrRoles);
    console.log(inputHidden.value)
}

function displayRoles(arrRoles)
{
    listRoles.textContent = "";
    arrRoles.forEach(strRole =>
    {
        const strTemplateItem = `<li id = ${strRole}> ${strRole} </li>`;
        listRoles.insertAdjacentHTML("afterBegin", strTemplateItem);
    });
}

function validateFieldsAndSubmit(event)
{
    event.preventDefault();
    const strPasswordOne = document.getElementById("passwordOne").value;
    const strPasswordTwo = document.getElementById("passwordTwo").value;
    console.log(`Roles Length`, setRoles.size)
    console.log(strPasswordOne)
    console.log(strPasswordTwo)
    console.log(inputHidden)
    if (strPasswordOne === strPasswordTwo && setRoles.size > 0)
    {
        formAddAccount.submit();
//        formAddAccount.submit();
    }
    else
    {
        divError.textContent = "";
        const strTemplateError = "<h2 id = error> Invalid Entry: Please Check your Input! </h2>";
        divError.insertAdjacentHTML("afterBegin", strTemplateError);
        return false
    }
}

const btnAddRole = document.getElementById("btn_add_role");
const btnAddAccount = document.getElementById("btn_add_account");
const listRoles = document.getElementById("role_list");
const selectRoles = document.getElementById("roles");
const inputPasswordOne = document.getElementById("passwordOne");
const inputPasswordTwo = document.getElementById("passwordTwo");
const formAddAccount = document.getElementById("add_user_form");
const divError = document.getElementById("error-message");

const inputHidden = document.getElementById("list_roles");

const setRoles = new Set();

if (btnAddRole)
    btnAddRole.addEventListener("click", addAndDisplayRole);

btnAddAccount.addEventListener("click", validateFieldsAndSubmit);
console.log(btnAddAccount);