;(function(){
	if(typeof MM === "undefined") {
      var MM = {};
      window.MM = MM;
    }

    //cookie 读取
    MM.getCookie = function(name) {
        var cookieValue = null;
        if(document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for(var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                if(cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = MM.getCookie('csrftoken');
    function csrfSafeMethod(method) {
        return(/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        // obviates need for sameOrigin test
        crossDomain: false,
        cache: false,
        //解决IE浏览器下缓存的问题
        contentType: "application/x-www-form-urlencoded; charset=UTF-8",
        // Ajax CSRFToken处理
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        //Ajax 错误处理
        ajaxError: function(event, jqxhr) {
            if(jqxhr.status !== 0) {
                alert(jqxhr.status);
            }
        }
    });

    MM.ajaxPost = function(url,data,fn){
        $.ajax({
            url: url,
            type: "post",
            dataType: "json",
            data: $.toJSON(data),
            success: fn
        })
    };

    //parse to Date object (only date)
    MM.parseDate = function(d) {
        if(typeof(d) === 'object') {
            return d;
        } else if(typeof(d) === 'string' && d.indexOf('-')) {
            if(d.indexOf(' ')){
                d = d.split(' ')[0];
            }
            var da = d.split('-');
            return new Date(da[0], da[1] - 1, da[2]);
        } else  {
            return new Date(d);
        }
    }
    //获取偏移日期
    MM.getOffsetDate = function(base, offset) {
        base = MM.parseDate(base);
        return new Date(base.getTime() + offset * 24 * 3600 * 1000);
    }
    //日期差值计算
    MM.diffDate = function(date1, date2) {
        date1 = MM.parseDate(date1);
        date2 = MM.parseDate(date2);
        date1 = new Date(date1.getFullYear(), date1.getMonth(), date1.getDate());
        date2 = new Date(date2.getFullYear(), date2.getMonth(), date2.getDate());
        return (date1.getTime() - date2.getTime()) / 1000 / 3600 / 24;
    }
    //格式化日期
    MM.formatDate = function(d, format) {
        d = MM.parseDate(d);
        var mon = d.getMonth() + 1;
        if(mon < 10) {
            mon = '0' + mon;
        }
        var day = d.getDate()
        if(day < 10) {
            day = '0' + day;
        }
        var hour = d.getHours();
        if(hour < 10){
            hour = '0' + hour;
        }
        var minute = d.getMinutes();
        if(minute < 10){
            minute = '0' + minute;
        }
        var second = d.getSeconds();
        if(second < 10){
            second = '0' + second;
        }
        var formatedDate = "";
        switch(format){
            case 'mm-dd':
                formatedDate = mon + '-' + day;
                break;
            case 'yyyy-mm':
                formatedDate = d.getFullYear() + '-' + mon;
                break;
            case 'yyyymmdd:hhmm':
                formatedDate = d.getFullYear() + "年" + (d.getMonth() + 1) + "月" + d.getDate() + "日 " + hour + ":" + minute;
                break;
            case 'yyyy-mm-dd hh:mm':
                formatedDate = d.getFullYear() + '-' + mon + '-' + day + " " + hour + ":" + minute;
                break;
            case 'yyyymmdd:hhmmss':
                formatedDate = d.getFullYear() + '-' + mon + '-' + day + " " + hour + ":" + minute + ":" + second;
                break;
            case 'mm-dd hhmmss':
                formatedDate = mon + '-' + day + " " + hour + ":" + minute + ":" + second;
                break;
            case 'hhmmss':
                formatedDate = hour + ":" + minute + ":" + second;
                break;
            default:
                formatedDate = d.getFullYear() + '-' + mon + '-' + day;
                break;
        }
        return formatedDate;
    };

    //获取字符串的实际长度，英文记1，中文记2
    MM.strlen = function(str){
        var len = 0;
        for (var i=0; i<str.length; i++) {
            var c = str.charCodeAt(i);
            if ((c >= 0x0001 && c <= 0x007e) || (0xff60<=c && c<=0xff9f)) {
                len++;
            } else {
                len+=2;
            }
        }
        return len;
    };

    //截取指定长度的中英文字符串
    MM.cutstr = function(str,len)
    {
        var str_length = 0;
        var str_len = 0;
        var str_cut = "",
        str_len = str.length;
        for(var i = 0;i < str_len; i++){
            var a = str.charAt(i);
            str_length++;
            if(escape(a).length > 4)
            {
            //中文字符的长度经编码之后大于4
            str_length++;
            }
            if(str_length <= len)
            {
                str_cut = str_cut.concat(a);
            }else{
                return str_cut;
            }
        }
        //如果给定字符串小于指定长度，则返回源字符串；
        if(str_length){
            return  str;
        }
        return str_cut;
    };

    (function(mm){
        var pub = {};

        pub.init = function(){
            initFixedElements();
            initEvents();
            initSignIn();
        }

        pub.addMask = function(){
            $('<div class="mask"><div class="mask-ctn"></div><div class="mask-content"><div class="close-btn"></div></div></div>').appendTo('body');
        }

        pub.deleteMask = function(){
            $(".mask").remove();
        }

        function initEvents(){
            $("body").delegate(".close-btn", "click", function(){
                $.cookie("newUser", "true");
                pub.deleteMask();
            });
        }

        //签到处理
        function initSignIn(){
            console.log( "cookie-od:" + $.cookie("od") );
            if( $.cookie("od") ){
                $('#sign_in').poshytip({
                    content: '<div class="tips-ctn">签到可以领取2个金币</div>',
                    className: 'tip-gray',
                    showTimeout: 0,
                    alignTo: 'target',
                    alignX: 'center',
                    live: true,
                    allowTipHover: true
                });
            }else{
                $('#sign_in').poshytip({
                    content: '<div class="tips-ctn">请先登录</div>',
                    className: 'tip-gray',
                    showTimeout: 0,
                    alignTo: 'target',
                    alignX: 'center',
                    live: true,
                    allowTipHover: true
                });
            }
        }

        //公共fixed浮动元素的处理
        function initFixedElements(){
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
            $("body").delegate("#scrollToTop", "click", function(){
                GoTop();
            });
        }

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

        mm.comm = pub;
    })(MM);

    $(function(){
        MM.comm.init();
    });
})();