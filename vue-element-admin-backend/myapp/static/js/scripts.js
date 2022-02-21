$(function () {
    const default_error_message = '服务器出错, 请重新启动!.';
    // 验证csrf保护
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader('X-CSRFToken', csrf_token);
            }
        }
    });
    // ajax错误提示
    $(document).ajaxError(function (event, request, settings) {
        const data = JSON.parse(request.responseText);
        let message = null;
        if (request.responseJSON && request.responseJSON.hasOwnProperty('message')) {
            message = request.responseJSON.message;
        } else if (request.responseText) {
            let IS_JSON = true;
            try {
            } catch (err) {
                IS_JSON = false;
            }
            if (IS_JSON && data !== undefined && data.hasOwnProperty('message')) {
                message = JSON.parse(request.responseText).message;
            } else {
                message = default_error_message;
            }
        } else {
            message = default_error_message;
        }
        toast(message, 'error');
    });

    let flash = null;

    //出现弹窗函数
    function toast(body, category) {
        clearTimeout(flash);
        const $toast = $('#toast');
        if (category === 'error') {
            $toast.css('background-color', 'red')
        } else {
            $toast.css('background-color', '#333')
        }
        $toast.text(body).fadeIn();
        flash = setTimeout(function () {
            $toast.fadeOut();
        }, 3000);
    }

    let hover_timer = null;

    // 展示悬窗用户信息
    function show_profile_popover(e) {
        const $el = $(e.target);
        hover_timer = setTimeout(function () {
            hover_timer = null;
            $.ajax({
                type: 'GET',
                url: $el.data('href'),
                success: function (data) {
                    $el.popover({
                        html: true,
                        content: data,
                        trigger: 'manual',
                        animation: false
                    });
                    $el.popover('show');
                    $('.popover').on('mouseleave', function () {
                        setTimeout(function () {
                            $el.popover('hide');
                        }, 200);
                    });
                }
            });
        }, 500);
    }

    // 隐藏悬窗用户信息
    function hide_profile_popover(e) {
        const $el = $(e.target);

        if (hover_timer) {
            clearTimeout(hover_timer);
            hover_timer = null;
        } else {
            setTimeout(function () {
                if (!$('.popover:hover').length) {
                    $el.popover('hide');
                }
            }, 200);
        }
    }

    // 更新粉丝数
    function update_followers_count(id) {
        const $el = $('#followers-count-' + id);
        $.ajax({
            type: 'GET',
            url: $el.data('href'),
            success: function (data) {
                $el.text(data.count);
            }
        });
    }

    // 更新收藏数
    function update_collectors_count(id) {
        $.ajax({
            type: 'GET',
            url: $('#collectors-count-' + id).data('href'),
            success: function (data) {
                console.log(data);
                $('#collectors-count-' + id).text(data.count);
            }
        });
    }

    // 更新通知数
    function update_notifications_count() {
        const $el = $('#notification-badge');
        $.ajax({
            type: 'GET',
            url: $el.data('href'),
            success: function (data) {
                if (data.count === 0) {
                    $('#notification-badge').hide();
                } else {
                    $el.show();
                    $el.text(data.count)
                }
            }
        });
    }

    // 用户关注函数
    function follow(e) {
        const $el = $(e.target);
        const id = $el.data('id');

        $.ajax({
            type: 'POST',
            url: $el.data('href'),
            success: function (data) {
                $el.prev().show();
                $el.hide();
                update_followers_count(id);
                toast(data.message);
            }
        });
    }

    // 用户取消关注函数
    function unfollow(e) {
        const $el = $(e.target);
        const id = $el.data('id');

        $.ajax({
            type: 'POST',
            url: $el.data('href'),
            success: function (data) {
                $el.next().show();
                $el.hide();
                update_followers_count(id);
                toast(data.message);
            }
        });
    }

    // 用户收藏文章函数
    function collect(e) {
        const $el = $(e.target).data('href') ? $(e.target) : $(e.target).parent('.collect-btn');
        const id = $el.data('id');

        $.ajax({
            type: 'POST',
            url: $el.data('href'),
            success: function (data) {
                $el.prev().show();
                $el.hide();
                update_collectors_count(id);
                toast(data.message);
            }
        });
    }

    // 用户取消收藏文章
    function uncollect(e) {
        const $el = $(e.target).data('href') ? $(e.target) : $(e.target).parent('.uncollect-btn');
        const id = $el.data('id');
        $.ajax({
            type: 'POST',
            url: $el.data('href'),
            success: function (data) {
                $el.next().show();
                $el.hide();
                update_collectors_count(id);
                toast(data.message);
            }
        });
    }

    // 悬浮框显示
    $('.profile-popover').hover(show_profile_popover.bind(this), hide_profile_popover.bind(this));
    // 用户关注
    $(document).on('click', '.follow-btn', follow.bind(this));
    $(document).on('click', '.unfollow-btn', unfollow.bind(this));
    // 用户收藏触发
    $(document).on('click', '.collect-btn', collect.bind(this));
    $(document).on('click', '.uncollect-btn', uncollect.bind(this));

    //
    // 确认删除弹窗
    $('#confirm-delete').on('show.bs.modal', function (e) {
        $('.delete-form').attr('action', $(e.relatedTarget).data('href'));
    });

    if (is_authenticated) {
        setInterval(update_notifications_count, 30000);
    }

    $("[data-toggle='tooltip']").tooltip({title: moment($(this).data('timestamp')).format('lll')})

});


