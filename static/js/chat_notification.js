
	startChatNotificationService()
	setOnChatNotificationScrollListener()
	// onChatNotificationsPaginationTriggerListener()
function submitNewChatNotificationToCache(notification){
		var chatCachedNotifList = [];
		var result = chatCachedNotifList.filter(function(n){
			return n['notification_id'] === notification['notification_id']
		})
		if(result.length == 0){
			chatCachedNotifList.push(notification)
			appendTopChatNotification(notification)
		}
		else{
			refreshChatNotificationsList(notification)
		}
	}
function handleNewChatNotificationsData(notifications){
		if(notifications.length > 0){
			clearNoChatNotificationsCard()
			notifications.forEach(notification => {

				submitNewChatNotificationToCache(notification)

				setChatNewestTimestamp(notification['timestamp'])
			})
		}
	}
function setChatNewestTimestamp(timestamp){
		element = document.getElementById("id_chat_newest_timestamp")
		current = element.innerHTML
		if(Date.parse(timestamp) > Date.parse(current)){
			element.innerHTML = timestamp
		}
		else if(current == "" || current == null || current == "undefined"){
			element.innerHTML = timestamp
		}
	}

function chatRedirect(url){
		window.location.href = url;
	}

//creating card for new messages
function setupChatNotificationsMenu(){
		var notificationContainer = document.getElementById("id_chat_notifications_container")
		if(notificationContainer != null){
			setupChatDropdownHeader()
			card = createChatNotificationCard("id_no_chat_notifications")
			var div = document.createElement("div")
			div.classList.add("d-flex", "flex-row", "align-items-start")

			span = document.createElement("span")
			span.classList.add("align-items-start", "pt-1", "m-auto")
			span.innerHTML = "You have no notifications."
			div.appendChild(span)
			card.appendChild(div)
			notificationContainer.appendChild(card)

			setChatNotificationsCount([])

		}
	}
function clearNoChatNotificationsCard(){
		var element = document.getElementById("id_no_chat_notifications")
		if(element != null && element != "undefined"){
			document.getElementById("id_chat_notifications_container").removeChild(element)
		}
	}
function createChatNotificationCard(cardId){
		var card = document.createElement("div")
		if(cardId != "undefined"){
			card.id = cardId
		}

		card.classList.add("d-flex", "flex-column", "align-items-start", "chat-card","p-4")
		card.onmouseover = function(){this.style.backgroundColor = '#f2f2f2'}
		card.onmouseout = function(){this.style.backgroundColor = '#ffffff'}
		return card

	}
function createChatProfileImageThumbnail(notification){
		img = document.createElement("img")
		img.classList.add("notification-thumbnail-image", "img-fluid", "rounded-circle", "mr-2")
		img.style.width = "36px"
		img.style.height = "36px"
		img.src = notification['from']['image_url']
		img.id = assignChatImgId(notification['notification_id'])
		return img
	}
function createChatTimestampElement(notification){
		var timestamp = document.createElement("p")
		timestamp.classList.add("small", "pt-2", "timestamp-text")
		timestamp.innerHTML = notification['natural_timestamp']
		timestamp.id = assignChatTimestampId(notification)
		return timestamp
	}

//unread chat notification element
function appendTopChatNotification(notification){
		switch(notification['notification_type']) {
			case "UnreadChatRoomMessages":
				chatNotificationContainer = document.getElementById("id_chat_notifications_container")
				card = createUnreadChatRoomMessagesElement(notification)
				if(chatNotificationContainer.childNodes.length > 2){
					// Append as the SECOND child. First child is the "go to chatroom" button
					var index = chatNotificationContainer.childNodes.length - 1
					chatNotificationContainer.insertBefore(card, chatNotificationContainer.childNodes[index]);
				}
				else {
					chatNotificationContainer.appendChild(card)
				}
				break;
			default:
				// code block
		}
	}
function appendBottomChatNotification(notification){
		switch(notification['notification_type']) {
			case "UnreadChatRoomMessages":
				chatNotificationContainer = document.getElementById("id_chat_notifications_container")
				card = createUnreadChatRoomMessagesElement(notification)
				chatNotificationContainer.appendChild(card)
				break;
			default:
				// code block
		}
	}

	function createUnreadChatRoomMessagesElement(notification){
		card = createChatNotificationCard()
		card.id = assignChatCardId(notification)
			card.addEventListener("click", function(){
				chatRedirect(notification['actions']['redirect_url'])
			});

		var div1 = document.createElement("div")
		div1.classList.add("d-flex", "flex-row", "align-items-start")
		div1.id = assignChatDiv1Id(notification)
		div1.style.cursor='pointer';

		img = createChatProfileImageThumbnail(notification)
		img.id = assignChatImgId(notification)
		div1.appendChild(img)

		var div2 = document.createElement("div")
		div2.classList.add("d-flex", "flex-column")
		div2.id = assignChatDiv2Id(notification)

		var title = document.createElement("span")
		title.classList.add("align-items-start")
		title.innerHTML = notification['from']['title']
		title.id = assignChatTitleId(notification)
		div2.appendChild(title)

		var chatRoomMessage = document.createElement("span")
		chatRoomMessage.id = assignChatroomMessageId(notification)
		chatRoomMessage.classList.add("align-items-start", "pt-1", "small", "notification-chatroom-msg")
		if(notification['verb'].length > 50){
			chatRoomMessage.innerHTML = notification['verb'].slice(0, 50) + "..."
		}
		else{
			chatRoomMessage.innerHTML = notification['verb']
		}
		div2.appendChild(chatRoomMessage)
		div1.appendChild(div2)
		card.appendChild(div1)
		card.appendChild(createChatTimestampElement(notification))
		return card
	}

function handleChatNotificationsData(notifications, new_page_number){
    	if(notifications.length > 0){
    		clearNoChatNotificationsCard()
    		notifications.forEach(notification => {
				submitNewChatNotificationToCache(notification)
				setChatNewestTimestamp(notification['timestamp'])
			})
			setChatPageNumber(new_page_number)
	    }
	}
function refreshChatNotificationsList(notification){
		notificationContainer = document.getElementById("id_chat_notifications_container")
		if(notificationContainer != null){
			divs = notificationContainer.childNodes
			divs.forEach(function(card){
				if(card.id == ("id_notification_" + notification['notification_id'])){
					if(notification['notification_type'] == "UnreadChatRoomMessages"){
						refreshUnreadChatRoomMessagesCard(card, notification)
					}
				}
			})
		}
	}
function refreshUnreadChatRoomMessagesCard(card, notification){
		card.childNodes.forEach(function(element){
			if(element.id == ("id_chat_div1_" + notification['notification_id'])){
				element.childNodes.forEach(function(child){
					if(child.id == ("id_chat_div2_" + notification['notification_id'])){
						child.childNodes.forEach(function(nextChild){
							if(nextChild.id == ("id_chat_title_" + notification['notification_id'])){
								nextChild.innerHTML = notification['from']['title']
							}
							if(nextChild.id == ("id_chat_message_" + notification['notification_id'])){
								// found chat message
								if(notification['verb'].length > 50){
									nextChild.innerHTML = notification['verb'].slice(0, 50) + "..."
								}
								else{
									nextChild.innerHTML = notification['verb']
								}
							}
						})
					}
				})
			}

			// TIMESTAMP
			if (element.id == ("id_timestamp_" + notification['notification_id'])){
				element.innerHTML = notification['natural_timestamp']
			}
		})
	}
function setChatPaginationExhausted(){
		setChatPageNumber("-1")
	}
function setChatPageNumber(pageNumber){
		document.getElementById("id_chat_page_number").innerHTML = pageNumber
	}
// function onChatNotificationsPaginationTriggerListener(){
// 		window.onscroll = function(ev) {
// 			// because of rounding we need to add 2. 1 might be OK but I'm using 2.
// 			if ((window.innerHeight + window.scrollY + 2) >= document.body.scrollHeight) {
// 				getNextChatNotificationsPage()
// 			}
// 		};
// 	}
function setOnChatNotificationScrollListener(){
		var menu = document.getElementById("id_chat_notifications_container")
		if(menu != null ){
			menu.addEventListener("scroll", function(e){
				if ((menu.scrollTop) >= (menu.scrollHeight - menu.offsetHeight)) {
				 getNextChatNotificationsPage()
				}
			});
		}

	}
function setChatNotificationsCount(count){
		var countElement = document.getElementById("id_chat_notifications_count")
		if(count > 0){
			countElement.style.background = "red"
			countElement.style.display = "block"
			countElement.innerHTML = count
		}
		else{
			countElement.style.background = "transparent"
			countElement.style.display = "none"
		}
	}

function startChatNotificationService(){
		if("{{request.user.is_authenticated}}" == "True"){
			setInterval(getNewChatNotifications(), CHAT_NOTIFICATION_INTERVAL)
			setInterval(getUnreadChatNotificationsCount(), CHAT_NOTIFICATION_INTERVAL)
		}
	}
function assignChatDiv1Id(notification){
		return "id_chat_div1_" + notification['notification_id']
	}
function assignChatImgId(notification){
		return "id_chat_img_" + notification['notification_id']
	}
function assignChatTitleId(notification){
		return "id_chat_title_" + notification['notification_id']
	}
function assignChatroomMessageId(notification){
		return "id_chat_message_" + notification['notification_id']
	}
function assignChatDiv2Id(notification){
		return "id_chat_div2_" + notification['notification_id']
	}
function assignChatTimestampId(notification){
		return "id_timestamp_" + notification['notification_id']
	}
function assignChatCardId(notification){
		return "id_notification_" + notification['notification_id']
	}
function setChatInitialTimestamp(){
		// ('%Y-%m-%d %H:%M:%S.%f')
		var today = new Date();
		var date = today.getFullYear() + "-01-01 01:00:00.000000"
		document.getElementById("id_chat_newest_timestamp").innerHTML = date
	}
setChatInitialTimestamp()
