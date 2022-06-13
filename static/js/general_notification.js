
	const GENERAL_NOTIFICATION_INTERVAL = 1800
	const GENERAL_NOTIFICATION_TIMEOUT = 1800
  const CHAT_NOTIFICATION_INTERVAL = 30

	setOnGeneralNotificationScrollListener()

	var generalCachedNotifList = [];
	function submitGeneralNotificationToCache(notification){
		var result = generalCachedNotifList.filter(function(n){
			return n['notification_id'] === notification['notification_id']
		})
		if(result.length == 0){
			generalCachedNotifList.push(notification)
			appendBottomGeneralNotification(notification)
		}
		else{
			refreshGeneralNotificationsList(notification)
		}
	}
	function refreshGeneralNotificationsList(notification){
		notificationContainer = document.getElementById("id_general_notifications_container")

		if(notificationContainer != null){
			divs = notificationContainer.childNodes

			divs.forEach(function(card){
				// card
				if(card.id == ("id_notification_" + notification['notification_id'])){

					switch(notification['notification_type']) {

						case "FriendRequest":
							refreshFriendRequestCard(card, notification)
							break;

						case "FriendList":
							refreshFriendListCard(card, notification)
							break;

						default:
							// code block
					}
				}
			})
		}
	}
	function handleGeneralNotificationsData(notifications, new_page_number){
		if(notifications.length > 0){
			clearNoGeneralNotificationsCard()
			notifications.forEach(notification => {

				submitGeneralNotificationToCache(notification)

				setGeneralOldestTimestamp(notification['timestamp'])
				setGeneralNewestTimestamp(notification['timestamp'])
			})
			setGeneralPageNumber(new_page_number)
		}
	}
	function handleNewGeneralNotificationsData(notifications){
    	if(notifications.length > 0){
    		clearNoGeneralNotificationsCard()
    		notifications.forEach(notification => {

    			submitNewGeneralNotificationToCache(notification)

				setGeneralOldestTimestamp(notification['timestamp'])
				setGeneralNewestTimestamp(notification['timestamp'])
			})
	    }
	}
	function refreshGeneralNotificationsData(notifications){
		if(notifications.length > 0){
			clearNoGeneralNotificationsCard()
			notifications.forEach(notification => {

				submitGeneralNotificationToCache(notification)

				setGeneralOldestTimestamp(notification['timestamp'])
				setGeneralNewestTimestamp(notification['timestamp'])
			})
		}
	}
	function appendTopGeneralNotification(notification){

		switch(notification['notification_type']) {

			case "FriendRequest":
				notificationContainer = document.getElementById("id_general_notifications_container")
				card = createFriendRequestElement(notification)
				notificationContainer.insertBefore(card, notificationContainer.childNodes[0]);
				break;

			case "FriendList":
				notificationContainer = document.getElementById("id_general_notifications_container")
				card = createFriendListElement(notification)
				notificationContainer.insertBefore(card, notificationContainer.childNodes[0]);
				break;

			default:
				// code block
		}

		// preloadImage(notification['from']['image_url'], assignGeneralImgId(notification))
	}
	function appendBottomGeneralNotification(notification){

		switch(notification['notification_type']) {

			case "FriendRequest":
				notificationContainer = document.getElementById("id_general_notifications_container")
				card = createFriendRequestElement(notification)
				notificationContainer.appendChild(card)
				break;

			case "FriendList":
				notificationContainer = document.getElementById("id_general_notifications_container")
				card = createFriendListElement(notification)
				notificationContainer.appendChild(card)
				break;

			default:
				// code block
		}
		// preloadImage(notification['from']['image_url'], assignGeneralImgId(notification))
	}
	function refreshFriendRequestCard(card, notification){
		card.childNodes.forEach(function(element){

			// DIV1
			if(element.id == ("id_general_div1_" + notification['notification_id'])){
				element.childNodes.forEach(function(child){
					if(child.id == ("id_general_verb_" + notification['notification_id'])){
						// found verb
						child.innerHTML = notification['verb']
					}
				})
			}

			// DIV2
			if (element.id == ("id_general_div2_" + notification['notification_id'])){
				if(notification['is_active'] == "True"){
						// do nothing
				}
				else{
					// remove buttons b/c it has been answered
					card.removeChild(element)
				}
			}

			// TIMESTAMP
			if (element.id == ("id_timestamp_" + notification['notification_id'])){
				element.innerHTML = notification['natural_timestamp']
			}
		})
	}
	function refreshFriendListCard(card, notification){
		card.childNodes.forEach(function(element){

			// DIV1
			if(element.id == ("id_general_div1_" + notification['notification_id'])){
				element.childNodes.forEach(function(child){
					if(child.id == ("id_general_verb_" + notification['notification_id'])){
						// found verb
						child.innerHTML = notification['verb']
					}
				})
			}

			// TIMESTAMP
			if (element.id == ("id_timestamp_" + notification['notification_id'])){
				element.innerHTML = notification['natural_timestamp']
			}
		})
	}
	function createFriendListElement(notification){
		card = createGeneralNotificationCard()
		card.id = assignGeneralCardId(notification)
		card.addEventListener("click", function(){
			generalRedirect(notification['actions']['redirect_url'])
		})

		var div1 = document.createElement("div")
		div1.classList.add("d-flex", "flex-row", "align-items-start")
		div1.id = assignGeneralDiv1Id(notification)

		img = createGeneralProfileImageThumbnail(notification)
		div1.appendChild(img)

		span = document.createElement("span")
		span.classList.add("align-items-start", "pt-1", "m-auto")
		if(notification['verb'].length > 50){
			span.innerHTML = notification['verb'].slice(0, 50) + "..."
		}
		else{
			span.innerHTML = notification['verb']
		}
		span.id = assignGeneralVerbId(notification)
		div1.appendChild(span)
		card.appendChild(div1)
		card.appendChild(createGeneralTimestampElement(notification))

		return card
	}
	function createFriendRequestElement(notification){
		card = createGeneralNotificationCard()
		card.id = assignGeneralCardId(notification)
		card.addEventListener("click", function(){
			generalRedirect(notification['actions']['redirect_url'])
		})

		// Is the friend request PENDING? (not answered yet)
		if(notification['is_active'] == "True"){

			//console.log("found an active friend request")
			div1 = document.createElement("div")
			div1.classList.add("d-flex", "flex-row", "align-items-start")
			div1.id = assignGeneralDiv1Id(notification)

			img = createGeneralProfileImageThumbnail(notification)
			div1.appendChild(img)

			span = document.createElement("span")
			span.classList.add("m-auto")
			span.innerHTML = notification['verb']
			span.id = assignGeneralVerbId(notification)
			div1.appendChild(span)
			card.appendChild(div1)

			div2 = document.createElement("div")
			div2.classList.add("d-flex", "flex-row", "mt-2")
			div2.id = assignGeneralDiv2Id(notification)

			pos_action = document.createElement("a")
			pos_action.classList.add("btn", "btn-primary", "mr-2")
			pos_action.href = "#"
			pos_action.innerHTML = "Accept"
			pos_action.addEventListener("click", function(e){
				e.stopPropagation();
				sendAcceptFriendRequestToSocket(notification['notification_id'])
			})
			pos_action.id = assignGeneralPosActionId(notification)
			div2.appendChild(pos_action)

			neg_action = document.createElement("a")
			neg_action.classList.add("btn", "btn-secondary")
			neg_action.href = "#"
			neg_action.innerHTML = "Decline"
			neg_action.addEventListener("click", function(e){
				e.stopPropagation();
				sendDeclineFriendRequestToSocket(notification['notification_id'])
			})
			neg_action.id = assignGeneralNegActionId(notification)
			div2.appendChild(neg_action)
			card.appendChild(div2)
		}
		// The friend request has been answered (Declined or accepted)
		else{
			var div1 = document.createElement("div")
			div1.classList.add("d-flex", "flex-row", "align-items-start")
			div1.id = assignGeneralDiv1Id(notification)

			img = createGeneralProfileImageThumbnail(notification)
			img.id = assignGeneralImgId(notification)
			div1.appendChild(img)

			span = document.createElement("span")
			span.classList.add("m-auto")
			span.innerHTML = notification['verb']
			span.id = assignGeneralVerbId(notification)
			div1.appendChild(span)
			card.appendChild(div1)
		}
		card.appendChild(createGeneralTimestampElement(notification))

		return card
	}
	function setupGeneralNotificationsMenu(){
		var notificationContainer = document.getElementById("id_general_notifications_container")

		if(notificationContainer != null){
			card = createGeneralNotificationCard("id_no_general_notifications")

			var div = document.createElement("div")
			div.classList.add("d-flex", "flex-row", "align-items-start")

			span = document.createElement("span")
			span.classList.add("align-items-start", "pt-1", "m-auto")
			span.innerHTML = "You have no notifications."
			div.appendChild(span)
			card.appendChild(div)
			notificationContainer.appendChild(card)
		}
	}
	function clearNoGeneralNotificationsCard(){
		var element = document.getElementById("id_no_general_notifications")
		if(element != null && element != "undefined"){
			document.getElementById("id_general_notifications_container").removeChild(element)
		}
	}
	function createGeneralNotificationCard(cardId){
		var card = document.createElement("div")
		if(cardId != "undefined"){
			card.id = cardId
		}
		card.classList.add("d-flex", "flex-column", "align-items-start", "general-card", "p-4")
		return card
	}
	function createGeneralProfileImageThumbnail(notification){
		var img = document.createElement("img")
		img.classList.add("notification-thumbnail-image", "img-fluid", "rounded-circle", "mr-2")
		img.src = "{% static 'images/bugambilaya.jpg' %}"
		img.id = assignGeneralImgId(notification)
		return img
	}
	function createGeneralTimestampElement(notification){
		var timestamp = document.createElement("p")
		timestamp.classList.add("small", "pt-2", "timestamp-text")
		timestamp.innerHTML = notification['natural_timestamp']
		timestamp.id = assignGeneralTimestampId(notification)
		return timestamp
	}
	function updateGeneralNotificationDiv(notification){
		notificationContainer = document.getElementById("id_general_notifications_container")

		if(notificationContainer != null){
			divs = notificationContainer.childNodes

			divs.forEach(function(element){
				if(element.id == ("id_notification_" + notification['notification_id'])){

					// Replace current div with updated one
					updatedDiv = createFriendRequestElement(notification)
					element.replaceWith(updatedDiv)
				}
			})
		}
	}
	function setOnGeneralNotificationScrollListener(){
		var menu = document.getElementById("id_general_notifications_container")
		if(menu != null ){
			menu.addEventListener("scroll", function(e){

				if ((menu.scrollTop) >= (menu.scrollHeight - menu.offsetHeight)) {
					getNextGeneralNotificationsPage()
				}
			});
		}
	}
	function setGeneralPaginationExhausted(){
		// console.log("general pagination exhausted.")
		setGeneralPageNumber("-1")
	}
	function setGeneralPageNumber(pageNumber){
		document.getElementById("id_general_page_number").innerHTML = pageNumber
	}
	function setGeneralOldestTimestamp(timestamp){
		element = document.getElementById("id_general_oldest_timestamp")
		current = element.innerHTML
		if(Date.parse(timestamp) < Date.parse(current)){
			element.innerHTML = timestamp
		}
	}
	function setGeneralNewestTimestamp(timestamp){
		element = document.getElementById("id_general_newest_timestamp")
		current = element.innerHTML
		if(Date.parse(timestamp) > Date.parse(current)){
			element.innerHTML = timestamp
		}
		else if(current == ""){
			element.innerHTML = timestamp
		}
	}

  //for general notification
	// function setUnreadGeneralNotificationsCount(count){
	// 	var countElement = document.getElementById("id_general_notifications_count")
	// 	if(count > 0){
	// 		countElement.style.background = "red"
	// 		countElement.style.display = "block"
	// 		countElement.innerHTML = count
	// 	}
	// 	else{
	// 		countElement.style.background = "transparent"
	// 		countElement.style.display = "none"
	// 	}
	// }

	function startGeneralNotificationService(){
		if("{{request.user.is_authenticated}}" == "True"){
			setInterval(refreshGeneralNotifications, GENERAL_NOTIFICATION_INTERVAL)
			setInterval(getNewGeneralNotifications, GENERAL_NOTIFICATION_INTERVAL)
			setInterval(getUnreadGeneralNotificationsCount, GENERAL_NOTIFICATION_INTERVAL)
		}
	}
	function generalRedirect(url){
		window.location.href = url
	}
	function assignGeneralDiv1Id(notification){
		return "id_general_div1_" + notification['notification_id']
	}
	function assignGeneralImgId(notification){
		return "id_general_img_" + notification['notification_id']
	}
	function assignGeneralVerbId(notification){
		return "id_general_verb_" + notification['notification_id']
	}
	function assignGeneralDiv2Id(notification){
		return "id_general_div2_" + notification['notification_id']
	}
	function assignGeneralPosActionId(notification){
		return "id_general_pos_action_" + notification['notification_id']
	}
	function assignGeneralNegActionId(notification){
		return "id_general_neg_action_" + notification['notification_id']
	}
	function assignGeneralTimestampId(notification){
		return "id_timestamp_" + notification['notification_id']
	}
	function assignGeneralCardId(notification){
		return "id_notification_" + notification['notification_id']
	}
	function setInitialTimestamp(){
		// ('%Y-%m-%d %H:%M:%S.%f')
		var today = new Date();
		var month = today.getMonth()+1
		if(month.toString().length == 1){
			month = "0" + month
		}
		var day = today.getDate()
		if(day.toString().length == 1){
			day = "0" + day
		}
		var hours = today.getHours()
		if(hours.toString().length == 1){
			hours = "0" + hours
		}
		var minutes = today.getMinutes()
		if(minutes.toString().length == 1){
			minutes = "0" + minutes
		}
		var seconds = today.getSeconds()
		if(seconds.toString().length == 1){
			seconds = "0" + seconds
		}
		var ms = "000000"
		var date = today.getFullYear()+'-'+month+'-'+day + " " + hours + ":" + minutes + ":" + seconds + "." + ms
		document.getElementById("id_general_oldest_timestamp").innerHTML = date
		document.getElementById("id_general_newest_timestamp").innerHTML = date
	}

	setInitialTimestamp()
