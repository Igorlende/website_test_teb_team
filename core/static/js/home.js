async function fetchAsyncJson(url, options) {
  const response = await fetch(url, options);
  if (!response.ok) {
    return { ok: false, status: response.status };
  }
  const data = await response.json();
  return { ok: true, data: data, status: response.status };
}


async function getCustomDate() {
  let dateFrom = document.getElementsByName('calendar1')[0].value;
  let dateTo = document.getElementsByName('calendar2')[0].value;
  //document.body.innerHTML += '<div class="loader"></div>';
  let div = document.createElement('div');
  div.classList.add("loader");
  div.classList.add("m-1");
  document.body.appendChild(div);
  let url = window.location.origin + "/api/get_clicks_and_conversations_by_custom_date?";
  const options = { method: "GET", credentials: 'include' };
  url = url + "from=" + dateFrom + "&to=" + dateTo;
  let result = await fetchAsyncJson(url, options);
  //console.log(result);
  if (result.ok) {
    let clicks = document.getElementById("clicks");
    let conversations = document.getElementById("conversations");
    clicks.innerHTML = result.data.clicks;
    conversations.innerHTML = result.data.conversations;
  }
  document.getElementsByClassName('loader m-1')[0].remove();

}


function addCalendar() {
  document.body.innerHTML += '<div class="calendar m-2">From <input type="date" name="calendar1"> to <input type="date" name="calendar2"> <button type="button" class="btn btn-secondary m-3" id="find">Find</button> </div>';
  let divWithMenu = document.getElementsByClassName("dropdown-menu show");
  divWithMenu[0].classList.remove("show");
  let btnFind = document.getElementById("find");
  btnFind.addEventListener("click", getCustomDate, false);
}


let custom = document.getElementById("custom");
custom.addEventListener("click", addCalendar, false);