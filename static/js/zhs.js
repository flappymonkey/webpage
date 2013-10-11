$(function(){

	var window_width = $(window).width();
	var right = (window_width - 960)/2 - 48;
	if(right < 10){
		right = 10;
	}
	$("#scrollToTop").css("right", right);
	$(window).scroll(function(event) {
		var scrollTop = $(window).scrollTop();
		if(scrollTop == 0){
			$(".top-bar").css("position","");
		}else{
			$(".top-bar").css("position","fixed");
		}
		if(scrollTop > 500){
			$("#scrollToTop").show();
		}else{
			$("#scrollToTop").hide();
		}
	});
	function addMask(){
		$('<div class="mask"><div class="mask-ctn"></div><div class="mask-content"><div class="close-btn"></div></div></div>').appendTo('body');
	}
	function deleteMask(){
		$(".mask").remove();
	}

	setPaginaviBar(0);
	function setPaginaviBar(search_type){
		MM.ajaxPost("/get_feeds_count",{search_type:search_type},function(ret_data){
			var mole = ret_data.data % 10;
			var page = Math.floor( ret_data.data / 10 );
			$("#pagination").myPagination({
				pageCount: mole ? page + 1 : page,
				pageNumber: 10,
				panel: {
		            tipInfo_on: true,
		            tipInfo: '  跳{input}/{sumPage}页',
		            tipInfo_css: {
		              width: '25px',
		              height: "20px",
		              border: "2px solid #f0f0f0",
		              padding: "0 0 0 5px",
		              margin: "0 5px 0 5px",
		              color: "#48b9ef"
		            }
		          },
				ajax: {
					on: false,
					onClick: function(page) {
						if( !$.cookie("newUser") ){
							addMask();
						}
						MM.ajaxPost("ajax_get_feeds",{page_num: page, search_type: search_type},function(ret_data){
							var items = generateItems(ret_data.data);
							$(".feeds-ctn").html( $("#feedItemTmpl").tmpl(items) );
							$(window).scrollTop(0);
						});
					}
				}
			});
		})
	};
	$("body").delegate(".close-btn", "click", function(){
		$.cookie("newUser", "true");
		deleteMask();
	});
	//为元素绑定事件，此处只为提供复制功能的flash插件所用
	function bind( obj, type, fn ) {
		if ( obj.attachEvent ) {
			obj['e'+type+fn] = fn;
			obj[type+fn] = function(){obj['e'+type+fn]( window.event );}
			obj.attachEvent( 'on'+type, obj[type+fn] );
		} else{
			obj.addEventListener( type, fn, false );
		} 
	}

	var clip = new ZeroClipboard.Client();
	var html = clip.getHTML( 100, 28 );
	$(".clipboard").html(html);
	bind(clip,'mouseUp',function(client){
		client.setText("314107031");
	});
	
	bind(clip,'complete',function(){
		alert("群号复制成功");
	});

	var search_type = 0;
	var get_page_times = 1;
	var isLoading = false;
	var isEnd = false;
	var cat_dict = {
		0 : "全部",
		1 : "白菜价",
		2 : "强烈值得买",
		3 : "其它"
	}

	// $(".weixin").hover(function() {
	// 	$(this).find(".icon").addClass("hover");
	// 	$(this).find(".detail").addClass("hover");
	// }, function() {
	// 	$(this).find(".icon").removeClass("hover");
	// 	$(this).find(".detail").removeClass("hover");
	// });
	$(".qqqun").hover(function() {
		setTimeout(function(){
			clip.reposition();
		},500);
	});

	// $("#lowest").hover(function() {
	// 	$(this).animate({width:'80px'},function(){
	// 		$(this).text("强烈值得买");
	// 	});
		
	// }, function() {
	// 	$(this).text("最低");
	// 	$(this).animate({width:'40px'});
	// });
	$("#lowest").click(function(event) {
		var self = this;
		MM.ajaxPost("/ajax_get_feeds",{page_num: 1, search_type: 2}, function(ret_data){
			$(window).scrollTop(0);
			search_type = 2;
			get_page_times = 1;
			isEnd = false;
			var items = generateItems(ret_data.data);
			$(".feeds-ctn").html( $("#feedItemTmpl").tmpl(items) );
			$("#lowest").addClass("on");
			$("#cheap, #all").removeClass("on");
		})
		setPaginaviBar(2)
	});

	// $("#cheap").hover(function() {
	// 	$(this).animate({width:'80px'}, function(){
	// 		$(this).text("白菜价");
	// 	});
	// }, function() {
	// 	$(this).animate({width:'40px'});
	// 	$(this).text("菜价");
	// });
	$("#cheap").click(function(event) {
		var self = this;
		MM.ajaxPost("/ajax_get_feeds",{page_num: 1, search_type: 1}, function(ret_data){
			$(window).scrollTop(0);
			search_type = 1;
			get_page_times = 1;
			isEnd = false;
			var items = generateItems(ret_data.data);
			$(".feeds-ctn").html( $("#feedItemTmpl").tmpl(items) );
			$("#cheap").addClass("on");
			$("#lowest, #all").removeClass("on");
		})
		setPaginaviBar(1);
	});

	// $("#all").hover(function() {
	// 	$(this).animate({width:'80px'}, function(){
	// 		$(this).text("查看全部");
	// 	});
	// }, function() {
	// 	$(this).animate({width:'40px'});
	// 	$(this).text("全部");
	// });
	$("#all").click(function(event) {
		var self = this;
		MM.ajaxPost("/ajax_get_feeds",{page_num: 1, search_type: 0}, function(ret_data){
			$(window).scrollTop(0);
			search_type = 0;
			get_page_times = 1;
			isEnd = false;
			var items = generateItems(ret_data.data);
			$(".feeds-ctn").html( $("#feedItemTmpl").tmpl(items) );
			$("#all").addClass("on");
			$("#lowest, #cheap").removeClass("on");
		})
		setPaginaviBar(0);
	});

	$(".feeds-ctn").delegate(".type", 'click', function(){
		var text = $.trim( $(this).text() );
		console.log(text);
		if(text == "白菜价"){
			MM.ajaxPost("/ajax_get_feeds",{page_num: 1, search_type: 1}, function(ret_data){
				$(window).scrollTop(0);
				search_type = 1;
				get_page_times = 1;
				isEnd = false;
				var items = generateItems(ret_data.data);
				$(".feeds-ctn").html( $("#feedItemTmpl").tmpl(items) );
				$("#cheap").addClass("on");
				$("#lowest, #all").removeClass("on");
			});
			setPaginaviBar(1);
		}else if(text == "强烈值得买"){
			MM.ajaxPost("/ajax_get_feeds",{page_num: 1, search_type: 2}, function(ret_data){
				$(window).scrollTop(0);
				search_type = 2;
				get_page_times = 1;
				isEnd = false;
				var items = generateItems(ret_data.data);
				$(".feeds-ctn").html( $("#feedItemTmpl").tmpl(items) );
				$("#lowest").addClass("on");
				$("#cheap, #all").removeClass("on");
				$("#all").removeClass("on");
			});
			setPaginaviBar(2);
		}
		return false;
	})

	$(".feeds-ctn").delegate('.next-page', 'click', function(event) {
		$(".feeds-ctn .next-page").remove();
		$(".feeds-ctn").append('<div class="loading"><img src="/static/images/loading.gif" /></div>');
		isLoading = true;
		MM.ajaxPost("ajax_get_feeds",{page_num: 1 + get_page_times, search_type: search_type},function(ret_data){
			$(".feeds-ctn .loading").remove();
			var items = generateItems(ret_data.data);
			$(".feeds-ctn").append( $("#feedItemTmpl").tmpl(items) );
			isLoading = false;
			get_page_times++;
			if(items.length < 10){
				isEnd = true;
				$(".feeds-ctn").append('<div class="no-more">没有更多数据...</div>');
			}else{
				$(".feeds-ctn").append('<div class="next-page">下一页</div>');
			}
		});
	});

	$(".feeds-ctn").delegate(".deserve-icon", "click", function(){
		var self = this;
		var id = $(this).parent().attr("id");
		if( $.cookie(id) ){
			return;
		}
		MM.ajaxPost("/ajax_add_worth", {id:id}, function(ret_data){
			var number = $(self).prev().text() - 0 + 1;
			var offset = $(self).offset();
			$("<div class='add-one'></div>").css({top:offset.top - 20, left:offset.left}).appendTo('body').fadeOut(1000, function() {
				$(this).remove();
				$(self).prev().text(number);
			});
			$.cookie(id, "true");
			$(self).parent().addClass('clicked');
		});
	});
	$(".feeds-ctn").delegate(".undeserve-icon", "click", function(){
		var self = this;
		var id = $(this).parent().attr("id");
		if( $.cookie(id) ){
			return;
		}
		MM.ajaxPost("/ajax_add_bad", {id:id}, function(ret_data){
			var number = $(self).prev().text() - 0 + 1;
			var offset = $(self).offset();
			$("<div class='add-one'></div>").css({top:offset.top - 20, left:offset.left}).appendTo('body').fadeOut(1000, function() {
				$(this).remove();
				$(self).prev().text(number);
			});
			$.cookie(id, "true");
			$(self).parent().addClass('clicked');
		});
	});

	$(".feeds-ctn").delegate(".share-qqzone", "click", function(){
		var data = eval( '(' + $(this).parent().attr("data") + ')' );
		var s = [];
		s.push('url=' + encodeURIComponent(data["url"]||''));
		s.push('desc=' + encodeURIComponent(data["desc"]||''));
		s.push('pics=' + encodeURIComponent(data["pic"]||''));
		s.push('title=' + encodeURIComponent(data["title"]||''));
		s.push('summary=' + encodeURIComponent(data["text"]||''));
		window.open("http://sns.qzone.qq.com/cgi-bin/qzshare/cgi_qzshare_onekey?" + s.join('&'));
		return false;
	});

	$("body").delegate("#scrollToTop", "click", function(){
		// $(window).scrollTop(0);
		GoTop();
	});
	var timer;
	function GoTop(){ 
		timer=setInterval(runToTop,1); 
	} 
	function runToTop(){ 
		currentPosition=document.documentElement.scrollTop || document.body.scrollTop; 
		currentPosition-=200; 
		if(currentPosition>0) 
		{ 
		window.scrollTo(0,currentPosition); 
		} 
		else 
		{ 
		window.scrollTo(0,0); 
			clearInterval(timer); 
		} 
	} 


	function generateItems(items){
		for(var i = 0, length =  items.length; i < length; i++){
			items[i]["title"] = setHotTitle(items[i]["title"],items[i]["flush"]);
			items[i]["cat"] = items[i]["cat"][0];
			items[i]["our_cat"] = cat_dict[items[i]["our_cat"]];
			items[i]["descData"] = $.toJSON({
				url : "http://ztmhs.maimiaotech.com/redirect/?" + items[i]["img_link_id"],
				pic : "http://ztmhs.maimiaotech.com" + items[i]["img"],
				title : items[i]["title"],
				text : items[i]["desc"][0],
				desc : "【更多9块9包邮资讯】：http://user.qzone.qq.com/2937396129/main"
			});
			items[i]["desc"] = makeProductLink(items[i]["desc"], items[i]["desc_link"]);
		}
		return items;
	}

	function setHotTitle(title, flush){
		for(var i = 0, length = flush.length; i < length; i++){
			var hot = $.trim( flush[i] );
			title = title.replace(hot, "<strong>" + hot + "</strong>");
		}
		return title;
	}

	function makeProductLink(desc, desc_link){
		var detail_desc = "";
		for(var i = 0, length = desc.length; i < length; i++){
			detail_desc = detail_desc + "<p>" + desc[i] + "</p>";
		}
		for(var i = 0, length = desc_link.length; i < length; i++){
			detail_desc = detail_desc.replace(desc_link[i][0],'<a target="_blank" href="/redirect/?' + desc_link[i][1] + '">' + desc_link[i][0] + '</a>');
		}
		return detail_desc;
	}
});