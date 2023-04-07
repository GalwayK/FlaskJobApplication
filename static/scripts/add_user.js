"use strict";

function addAndDisplayRole(event)
{
    event.preventDefault();
    const strRole = selectRoles.value;
    setRoles.add(strRole);
    const arrRoles = Array.from(setRoles);
    displayRoles(arrRoles);
    inputHidden.value = arrRoles;
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
    console.log(setRoles.length)
    if (strPasswordOne === strPasswordTwo && setRoles.size > 0)
    {
        return true
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
const divError = document.getElementById("error_message");

const strTemplateHidden = "<input type = 'hidden' id = list_roles name = list_roles></input>";
formAddAccount.insertAdjacentHTML("beforeEnd", strTemplateHidden);
const inputHidden = document.getElementById("list_roles");
console.log(inputHidden)

const setRoles = new Set();

btnAddRole.addEventListener("click", addAndDisplayRole);
btnAddAccount.addEventListener("submit", validateFieldsAndSubmit);
