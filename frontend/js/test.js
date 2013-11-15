var templates = new function() {
    this.error  = Handlebars.compile($("#error-alert-template").html());
    this.member = Handlebars.compile($("#member-alert-template").html());
    this.guest  = Handlebars.compile($("#guest-alert-template").html());
    this.plistrow = Handlebars.compile($("#person-list-row-template").html());
};

function PersonList(id) {
    this.id = id;
};
PersonList.prototype.addPerson = function(person) {
    html = templates.plistrow(person);	// expects first and last
    $("#" + this.id + " table").append(html);
};

GuestList = new PersonList("guest-table");
MembersList = new PersonList("members-table");

var alertHandler = new function() {
    this.selector = "#alerts";
    this.count = 0;
    this.add_alert = function(alert) {
	$(this.selector).prepend(alert);
	this.count += 1;
    };
};

var swipeHandler = new function() {
    this.member = function(data) {
	var html = templates.member(data);
	alertHandler.add_alert(html);
    };
    this.error = function(data) {
	var html = templates.error(data);
	alertHandler.add_alert(html);
    };
    this.guest = function(data){
	console.log("Guest");
	var html = templates.guest(data);
	alertHandler.add_alert(html);
	GuestList.addPerson(data);
    };
};



$(document).ready(function () {
    var ws;
    var host = "localhost";
    var port = "8888";
    var uri = "/ws";
    
    ws = new WebSocket("ws://" + host + ":" + port + uri);
    
    ws.onmessage = function(evt) {
	console.log("received message");
	data = $.parseJSON(evt.data)
	if (data.type === "swipe") {
	    // TODO: replace with handler syntax
	    if (data.status === "error")
		swipeHandler.error(data);
	    else if (data.status === "guest")
		swipeHandler.guest(data);
	    else if (data.status === "member")
		swipeHandler.member(data);
	}
	    
    };
    
    ws.onclose = function(evt) {
    };
    
    ws.onopen = function(evt) {
    };
        
});

alertTimeout = function (wait, obj){
    setTimeout(function(){
        obj.fadeOut(1000, function() { $(this).remove()});
    }, wait);
};



