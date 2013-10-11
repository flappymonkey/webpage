;(function(mm){
	var pub = {};
	var req_type = $("#req_type").val() - 0;
	pub.init = function(){
		pub.initEvent();
		pub.initTimer();
		pub.setPaginaviBar(req_type, 1);
	}

	pub.initTimer = function(){
		$(".item").each(function(i, item){
			var timestamp, warnurl, warntime;
			if( $(item).hasClass("upcoming") ){
				timestamp = $(".timer", item).attr("start_time_stamp");
				var starttime = MM.formatDate(timestamp * 1000, "hhmmss");
				$(".starttime", item).text(starttime);
				$(".timer",item).text(starttime);
				var title = $(".desc", item).text();
				warntime = MM.formatDate(timestamp * 1000, "yyyy-mm-dd hh:mm");
				warnurl = "http://qzs.qq.com/snsapp/app/bee/widget/open.htm#content=”" + title + "“还有5分钟就要开始秒杀啦！GO！&time=" + warntime + "&advance=5&url=http://ztmhs.maimiaotech.com/seckill?req_type=1";
			}else{
				timestamp = $(".timer", item).attr("end_time_stamp");
				$(".timer",item).text(MM.formatDate(timestamp * 1000, "hhmmss"));
				warntime = MM.formatDate( MM.getOffsetDate(new Date(), 1) ) + " 10:00";
				warnurl = "http://qzs.qq.com/snsapp/app/bee/widget/open.htm#content=今天的秒杀已经开始了，要知道好价格的商品可是稍纵即逝哦！&time=" + warntime + "&advance=0&url=http://ztmhs.maimiaotech.com/seckill";
			}
			$(".qqwarn a", item).attr("href", warnurl);

			var id = $(item).attr("id");
			var endTime = new Date(timestamp*1000);
			updateTime(id, endTime);
		});
	}

	function generateItems(items){
		for(var i = 0, length = items.length; i < length; i++){
			items[i].title = $.trim( items[i].title )
			// if(MM.strlen(items[i].title) > 74){
			// 	items[i].title = MM.cutstr(items[i].title, 74) + "...";
			// }
			items[i].cur_price = items[i].cur_price == -1 ? -1 : items[i].cur_price/100;
			items[i].ori_price = items[i].ori_price == -1 ? -1 : items[i].ori_price/100;
			items[i].discount = items[i].discount == -1 ? -1 : items[i].discount/10;
		}
		$(".sec-kill-items").html( $("#seckillItemTmpl").tmpl(items) );
		pub.initTimer();
	}

	pub.initEvent = function(){
		$("#upcoming_btn").click(function(){
			if( !$(this).hasClass("on") ){
				req_type = 1;
				MM.ajaxPost("/ajax_get_seckills",{page_num: 1, req_type: req_type, order: 1},function(ret_data){
					generateItems(ret_data.data);
					pub.setPaginaviBar(req_type, 1);
				});
				$("#upcoming_btn").addClass("on");
				$("#sellout_btn").removeClass("on");
				$("#normal_btn").removeClass("on");
				$("#normal_btn i").removeClass("asc desc").addClass("normal");
			}
		});
		$("#sellout_btn").click(function(){
			if( !$(this).hasClass("on") ){
				req_type = 2;
				MM.ajaxPost("/ajax_get_seckills",{page_num: 1, req_type: req_type, order: 1},function(ret_data){
					generateItems(ret_data.data);
					pub.setPaginaviBar(req_type, 1);
				});
				$("#upcoming_btn").removeClass("on");
				$("#sellout_btn").addClass("on");
				$("#normal_btn").removeClass("on");
				$("#normal_btn i").removeClass("asc desc").addClass("normal");
			}
		});
		$("#normal_btn").click(function(){
			req_type = 3;
			if( $(this).hasClass("on") ){
				if( $("i",this).hasClass("asc") ){
					MM.ajaxPost("/ajax_get_seckills",{page_num: 1, req_type: req_type, order: -1},function(ret_data){
						generateItems(ret_data.data);
						pub.setPaginaviBar(req_type, -1);
					});
					$("#normal_btn i").removeClass("asc normal").addClass("desc");
				}else{
					MM.ajaxPost("/ajax_get_seckills",{page_num: 1, req_type: req_type, order: 1},function(ret_data){
						generateItems(ret_data.data);
						pub.setPaginaviBar(req_type, 1);
					});
					$("#normal_btn i").removeClass("normal desc").addClass("asc");
				}
			}else{
				MM.ajaxPost("/ajax_get_seckills",{page_num: 1, req_type: req_type, order: 1},function(ret_data){
					generateItems(ret_data.data);
					pub.setPaginaviBar(req_type, 1);
				});
				$("#upcoming_btn").removeClass("on");
				$("#sellout_btn").removeClass("on");
				$("#normal_btn").addClass("on");
				$("#normal_btn i").removeClass("normal").addClass("asc");
			}
		});
	}

	pub.setPaginaviBar = function(req_type, order){
		MM.ajaxPost("/get_seckills_count",{},function(ret_data){
			var mole = ret_data.data % 30;
			var page = Math.floor( ret_data.data / 30 );
			$("#pagination").myPagination({
				pageCount: mole ? page + 1 : page,
				pageNumber: 10,
				// panel: {
				// 	tipInfo_on: true,
				// 	tipInfo: '  跳{input}/{sumPage}页',
				// 	tipInfo_css: {
				// 		width: '25px',
				// 		height: "20px",
				// 		border: "2px solid #f0f0f0",
				// 		padding: "0 0 0 5px",
				// 		margin: "0 5px 0 5px",
				// 		color: "#48b9ef"
				// 	}
				// },
				ajax: {
					on: false,
					onClick: function(page) {
						if( !$.cookie("newUser") ){
							mm.comm.addMask();
						}
						MM.ajaxPost("/ajax_get_seckills",{page_num: page, req_type: req_type, order: order},function(ret_data){
							generateItems(ret_data.data);
							$(window).scrollTop(0);
						});
					}
				}
			});
		})
	};

	function updateTime(id, endTime){
		var endHour = endTime.getHours();
		var endMinute = endTime.getMinutes();
		var endSecond = endTime.getSeconds();
		var endDay
		var today = new Date();
		var nowHour = today.getHours();
		var nowMinute = today.getMinutes();
		var nowSecond = today.getSeconds();
		var hourleft = endHour - nowHour;
		var minuteleft = endMinute - nowMinute;
		var secondleft = endSecond - nowSecond;
		if (secondleft < 0)
		{
			secondleft = 60 + secondleft;
			minuteleft = minuteleft - 1;
		}
		if (minuteleft < 0)
		{
			minuteleft = 60 + minuteleft;
			hourleft = hourleft - 1;
		}
		if (hourleft < 0){
			hourleft = 24 + hourleft;
		}
		if( (endTime.getTime() - today.getTime()) <= 5*60*1000 ){ //5分钟内变为可点
			$("#" + id).addClass("in5min");
		}
		if (today >= endTime)
		{
			$("#" + id).removeClass("in5min");
			if( $("#" + id).hasClass("upcoming") ){
				$("#" + id + " .time-type").text("结束时间:");
				var timestamp = $("#" + id + " .timer").attr("end_time_stamp");
				$("#" + id + " .timer").text(MM.formatDate(timestamp * 1000, "hhmmss"));
				$("#" + id).removeClass("upcoming").addClass("normal");
				var newEndTime = new Date(timestamp*1000);
				setTimeout(function(){updateTime(id, newEndTime)},1000);
			}else{
				$("#" + id + " .time-type").text("已经结束");
				$("#" + id + " .timer").text("");
				warntime = MM.formatDate( MM.getOffsetDate(new Date(), 1) ) + " 10:00";
				warnurl = "http://qzs.qq.com/snsapp/app/bee/widget/open.htm#content=今天的秒杀已经开始了，要知道好价格的商品可是稍纵即逝哦！&time=" + warntime + "&advance=0&url=http://ztmhs.maimiaotech.com/seckill";
				$("#" + id + " .qqwarn a").attr("href", warnurl);
				$("#" + id).removeClass("normal").addClass("sellout");
			}
		}else{
			$("#" + id + " .timer").text( hourleft + '小时' + minuteleft + "分" + secondleft + "秒");
			setTimeout(function(){updateTime(id, endTime)},1000);
		}
	}

	mm.seckill = pub;
})(MM);