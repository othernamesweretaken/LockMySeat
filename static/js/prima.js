var BookedSeats = [];
var Columns1=["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"];
var c = parseInt(document.getElementById('columns').textContent);
var r = parseInt(document.getElementById('rows').textContent);
var Columns = []
for(i=0;i<c;i++){
	Columns.push(Columns1[i]);
}
var Rows=r;
var TotalSeats=Columns.length*Rows;

function convertIntToSeatNumbers(seats){
	var bookedSeats="";
	_.each(seats,function(seat){
		// var row=Rows[parseInt(parseInt(seat)/c)];
		// var column=parseInt(seat)%Columns;
		// if(column==0){
		// 	column=Columns;
		// }
		// if(_.indexOf(seats,seat)==seats.length-1){
		// 	bookedSeats=bookedSeats+row+column;
		// }
		// else{
		// 	bookedSeats=bookedSeats+row+column+",";
		// }
		var column = parseInt(parseInt(seat)%c)-1;
		if(column==-1){
		    column = parseInt(Columns.length - 1);
			column = Columns[column];
		    var row = parseInt(parseInt(seat)/c);
		}
		else{
                column = Columns[column];
                var row = parseInt(parseInt(seat)/c)+1;
		}

		if(_.indexOf(seats,seat)==seats.length-1){
			bookedSeats = bookedSeats+column+row;
		}
		else{
			bookedSeats=bookedSeats+column+row+",";
		}
	});
	return bookedSeats;
}


var InitialView = Backbone.View.extend({
	events:{
		"click #submitSelection": "submitForm"
	},
	submitForm : function(){
		var availableSeats=TotalSeats;
		var selectedNumberOfSeats=$('#seats').val();
		if(reservedseats!=null)
			availableSeats=TotalSeats-reservedseats.length;
		if(!$('#name').val()){
			$(".error").html("Name is required");
		}
		else if(!selectedNumberOfSeats){
			$(".error").html("Number of seats is required");
		}
		else if(parseInt(selectedNumberOfSeats)>availableSeats){
			$(".error").html("You can only select "+availableSeats+" seats")
		}
		else
		{
			$(".error").html("");
			screenUI.showView();
		}
	}
});
var initialView = new InitialView({el:$('.selectionForm')});

var ScreenUI=Backbone.View.extend({
	events:{
		"click .empty-seat,.booked-seat":"toggleBookedSeat",
		"click #confirmSelection":"bookTickets"
	},
	initialize:function(){
		var tableheaderTemplate = _.template($("#table-screen-header").html());
		var tableBodyTemplate=_.template($("#table-screen-body").html());
		var data={"rows":Rows,"columns":Columns};
		$("#screen-head").after(tableheaderTemplate(data));
		$("#screen-body").after(tableBodyTemplate(data));
	},
	hideView:function(){
		$(this.el).hide();
	},
	showView:function(){
		$(this.el).show();
	},
	toggleBookedSeat:function(event){
		var id="#"+event.currentTarget.id;
		if($(id).attr('class')=='empty-seat' && BookedSeats.length<$('#seats').val()){
			BookedSeats.push(id.substr(1));
			$(id).attr('src','/static/img/booked-seat.png');
			$(id).attr('class','booked-seat');

		}
		else if($(id).attr('class')=='booked-seat'){
			BookedSeats=_.without(BookedSeats,id.substr(1));
			$(id).attr('src','/static/img/empty-seat.png');
			$(id).attr('class','empty-seat');
		}
	},
	updateTicketInfo:function(){
		var bookedSeats=convertIntToSeatNumbers(BookedSeats);
		$("#ticket-sold-info").append("<tr><td>"+$('#name').val()+"</td><td>"+$('#seats').val()+"</td><td>"+bookedSeats+"</td></tr>");
	},
	bookTickets:function(){
		if(BookedSeats.length==parseInt($('#seats').val())) {
			$(".error").text("");
					reservedseats=JSON.parse(localStorage.getItem('ReservedSeats'))||[];

			_.each(BookedSeats,function(bookedSeat){
				reservedseats.push(bookedSeat);
			});

			var nameSeatsJSON=JSON.parse(localStorage.getItem('NameSeatsJSON'))||{};
			nameSeatsJSON[$('#name').val()]=BookedSeats;
			localStorage.setItem('NameSeatsJSON',JSON.stringify(nameSeatsJSON));
			localStorage.setItem('ReservedSeats',JSON.stringify(reservedseats));
			this.updateTicketInfo();
			var items=[];
		    var json=JSON.parse(localStorage.getItem('NameSeatsJSON'));
            if(json!=null){
		_.each(json,function(key,value){
			var name=value;
			var number=key.length;
			var bookedSeats=convertIntToSeatNumbers(key);
			items.push({names:name,numbers:number,seats:bookedSeats});

		});
		$('#SeatsDisplay1').val(items[0].seats);
		$('#NumberDisplay1').val(items[0].numbers);
		$('#NameDisplay1').val(items[0].names);
		}
//			window.location.reload();
		}
		else{
			$(".error").html("Please select exactly "+ $('#seats').val()+" seats");
		}
	},
});

var screenUI = new ScreenUI({el:$('.screen-ui')});
screenUI.hideView();

var TicketInfo=Backbone.View.extend({
	initialize:function(){
		var items=[];
		var json=JSON.parse(localStorage.getItem('NameSeatsJSON'));
		if(json!=null){
		_.each(json,function(key,value){
			var name=value;
			var number=key.length;
			var bookedSeats=convertIntToSeatNumbers(key);
			items.push({names:name,numbers:number,seats:bookedSeats});

		});
//		$(#'SeatsDisplay1').val()

		var data={"items":items};

		var ticketInfoBody=_.template($("#table-ticket-info").html());
		$("#ticket-sold-info").html(ticketInfoBody(data));

		}
	}
});

var ticketInfo=new TicketInfo({el:$('.table-responsive')});

// window.onbeforeunload = function (e) {
//     window.onunload = function () {
//             window.localStorage.isMySessionActive = "false";
//     }
//     return undefined;
// };

// window.onload = function () {
//             window.localStorage.isMySessionActive = "true";
//// };
//});