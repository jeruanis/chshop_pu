function chatLogScrollListener(e) {
   var chatLog = document.getElementById("id_chat_log")
   if ((Math.abs(chatLog.scrollTop) + 2) >= (chatLog.scrollHeight - chatLog.offsetHeight)) {
     getRoomChatMessages()
    }
  }
function enableChatLogScrollListener(chatLogScrollListener){
   document.getElementById("id_chat_log").addEventListener("scroll", chatLogScrollListener);
 }
function disableChatLogScrollListener(chatLogScrollListener){
     document.getElementById("id_chat_log").removeEventListener("scroll", chatLogScrollListener())
   }
function handleUserInfoPayload(user_info){
  document.getElementById("id_other_username").innerHTML = user_info['username'].substring(0,1).toUpperCase() + user_info['username'].substring(1).toLowerCase();;
  }
function closeWebSocket(chatsocket){
    if(chatSocket != null){
      chatSocket.close()
      chatSocket = null
      clearChatLog()
      setPageNumber("1")
      disableChatLogScrollListener()
    }
  }
// can make a link going to friends profile, otheruser profile pic and username
function handleUserInfoPayload(user_info){
  document.getElementById("id_other_username").innerHTML = user_info['username'].substring(0,1).toUpperCase() + user_info['username'].substring(1).toLowerCase();;
  // document.getElementById("id_other_user_profile_pic").classList.remove("d-none")
  // document.getElementById("id_other_user_profile_pic").src = user_info['profile_pic']
  // disable the redirection to account of others
  // document.getElementById("id_user_info_container").href= "{% url 'view' user_id=53252623623632623 %}".replace("53252623623632623", user_info['id'])
  // preloadImage(user_info['profile_pic'], "id_other_user_profile_pic")
  }
function showClientErrorModal(message){
  document.getElementById("id_client_error_modal_body").innerHTML = message
  document.getElementById("id_trigger_client_error_modal").click()
}
function setPageNumber(pageNumber){
  document.getElementById("id_page_number").innerHTML = pageNumber
 }
//clear chat
function clearChatLog(){
  document.getElementById("id_chat_log").innerHTML = ""
 }
//set page number to -1
function setPaginationExhausted(){
  setPageNumber("-1")
}
//append messages if they are not exhausted
function handleMessagesPayload(messages, new_page_number){
  if(messages != null && messages != "undefined" && messages != "None"){
  // if(messages){ //rephrase
    setPageNumber(new_page_number)
    messages.forEach(function(message){
      appendChatMessage(message, true, false)
    })
  }
  else{
    setPaginationExhausted() // no more messages
  }
}
// animate the page on opening
const gotoBottom = function(id){
  var element = document.querySelector('html');
  target_top = element.scrollHeight - element.clientHeight;
  $('html, body').animate({scrollTop:target_top});
}
function createConnectedDisconnectedElement(msg, msd_id, profile_pic, user_id){
    if((msg == '{{room.user2.username}}'+'connected.')){

    } else if(msg == '{{room.user2.username}}'+'disconnected.') {
      document.getElementById('dot-online').classList.add('d-none')
      document.getElementById('dot-offline').classList.remove('d-none')
    }

    else if(msg == '{{room.user1.username}}'+'disconnected.') {
       document.getElementById('dot-online').classList.add('d-none')
       document.getElementById('dot-offline').classList.remove('d-none')
    }else if((msg == '{{room.user1.username}}'+'connected.')){

    }
}
function selectUser(user_id){
  var url = "{% url 'view' user_id=53252623623632623 %}".replace("53252623623632623", user_id);
 }
function displayChatroomLoadingSpinner(isDisplayed){
  var spinner = document.getElementById("id_chatroom_loading_spinner")
  if(isDisplayed){
    spinner.style.display = "block"
  }
  else{
    spinner.style.display = "none"
  }
}
function highlightFriend(userId){
      document.getElementById("id_friend_container_" + userId).style.background = "#c2c2c2";
    }
