
	// Correctly decide between ws:// and wss://
	const ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
	if (ws_scheme == 'wss')
			ws_path = ws_scheme + '://' + window.location.host + ":8001/";
	else
			ws_path = ws_scheme + '://' + window.location.host;
	const notificationSocket = new WebSocket(ws_path);
	notificationSocket.onmessage = function(message) {
		const data = JSON.parse(message.data);

		if(data.general_msg_type == 0){
			handleGeneralNotificationsData(data['notifications'], data['new_page_number'])
		}
		if(data.general_msg_type == 1){
			setGeneralPaginationExhausted()
		}
		if(data.general_msg_type == 2){
			refreshGeneralNotificationsData(data['notifications'])
		}
		if(data.general_msg_type == 3){
			handleNewGeneralNotificationsData(data['notifications'])
		}

		if(data.general_msg_type == 5){
			updateGeneralNotificationDiv(data['notifications'])
		}

		if(data.chat_msg_type == 10){
			handleChatNotificationsData(data['notifications'], data['new_page_number'])
		}
		if(data.chat_msg_type == 11){
			setChatPaginationExhausted()
		}
		if(data.chat_msg_type == 13){
			handleNewChatNotificationsData(data['notifications'])
		}
		if(data.chat_msg_type == 14){
			setChatNotificationsCount(data['count'])
		}
	}

	notificationSocket.onopen = function(e){
		// console.log("Notification Socket on open: " + e)
		//for general notification only
		// setupGeneralNotificationsMenu()
		// getFirstGeneralNotificationsPage()
		// getUnreadGeneralNotificationsCount()

		setupChatNotificationsMenu() //this calls the function for dropdownheader
		getFirstChatNotificationsPage()
	}

	notificationSocket.onerror = function(e){
		// console.log('Notification Socket error', e)
	}
	if (notificationSocket.readyState == WebSocket.OPEN) {
		// console.log("Notification Socket OPEN complete.")
	}
	else if (notificationSocket.readyState == WebSocket.CONNECTING){
		// console.log("Notification Socket connecting..")
	}

	function getUnreadChatNotificationsCount(){
			if("{{request.user.is_authenticated}}"){
				notificationSocket.send(JSON.stringify({
					"command": "get_unread_chat_notifications_count",
				}));
			}
		}
	function getNextChatNotificationsPage(){
			var pageNumber = document.getElementById("id_chat_page_number").innerHTML
			// -1 means exhausted or a query is currently in progress
			if(pageNumber != "-1"){
				notificationSocket.send(JSON.stringify({
					"command": "get_chat_notifications",
					"page_number": pageNumber,
				}));
			}
		}
	function getNewChatNotifications(){
			newestTimestamp = document.getElementById("id_chat_newest_timestamp").innerHTML
			// console.log("NEWEST TS: " + newestTimestamp)
			if("{{request.user.is_authenticated}}"){
				notificationSocket.send(JSON.stringify({
					"command": "get_new_chat_notifications",
					"newest_timestamp": newestTimestamp,
				}));
			}
		}
	function getFirstChatNotificationsPage(){
			if("{{request.user.is_authenticated}}"){
				notificationSocket.send(JSON.stringify({
					"command": "get_chat_notifications",
					"page_number": "1",
				}));
				getUnreadChatNotificationsCount()
			}
		}

		//nconsumers communication
		function getUnreadGeneralNotificationsCount(){
			if("{{request.user.is_authenticated}}"){
				notificationSocket.send(JSON.stringify({
					"command": "get_unread_general_notifications_count",
				}));
			}
		}
		function setGeneralNotificationsAsRead(){
			if("{{request.user.is_authenticated}}"){
				oldestTimestamp = document.getElementById("id_general_oldest_timestamp").innerHTML
				notificationSocket.send(JSON.stringify({
					"command": "mark_notifications_read",
				}));
				getUnreadGeneralNotificationsCount()
			}
		}
		function getFirstGeneralNotificationsPage(){
			if("{{request.user.is_authenticated}}"){
				notificationSocket.send(JSON.stringify({
					"command": "get_general_notifications",
					"page_number": "1",
				}));
			}
		}
		function sendAcceptFriendRequestToSocket(notification_id){
			notificationSocket.send(JSON.stringify({
				"command": "accept_friend_request",
				"notification_id": notification_id,
			}));
		}
		function sendDeclineFriendRequestToSocket(notification_id){
			notificationSocket.send(JSON.stringify({
				"command": "decline_friend_request",
				"notification_id": notification_id,
			}));
		}
		function getNextGeneralNotificationsPage(){
			var pageNumber = document.getElementById("id_general_page_number").innerHTML
			// -1 means exhausted or a query is currently in progress
			if("{{request.user.is_authenticated}}" && pageNumber != "-1"){
				notificationSocket.send(JSON.stringify({
					"command": "get_general_notifications",
					"page_number": pageNumber,
				}));
			}
		}
		function refreshGeneralNotifications(){
			oldestTimestamp = document.getElementById("id_general_oldest_timestamp").innerHTML
			newestTimestamp = document.getElementById("id_general_newest_timestamp").innerHTML
			if("{{request.user.is_authenticated}}"){
				notificationSocket.send(JSON.stringify({
					"command": "refresh_general_notifications",
					"oldest_timestamp": oldestTimestamp,
					"newest_timestamp": newestTimestamp,
				}));
			}
		}
		function getNewGeneralNotifications(){
			newestTimestamp = document.getElementById("id_general_newest_timestamp").innerHTML
			if("{{request.user.is_authenticated}}"){
				notificationSocket.send(JSON.stringify({
					"command": "get_new_general_notifications",
					"newest_timestamp": newestTimestamp,
				}));
			}
		}
