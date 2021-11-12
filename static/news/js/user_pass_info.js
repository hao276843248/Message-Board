var page_index = 1
$(function () {
    // 首次进入
    updateData(page_index)
    $(".pass_info").submit(function (e) {
        e.preventDefault();

        var params = {};
        $(this).serializeArray().map(function (x) {
            params[x.name] = x.value;
        });

        $.ajax({
            url: "/input",
            type: "post",
            contentType: "application/json",
            data: JSON.stringify(params),
            success: function (resp) {
                if (resp.errno === 0) {
                    updateData(1)
                } else {
                    alert(resp.errno)
                }
            }
        })
    })

    $(".login_form").submit(function (e) {
        e.preventDefault();

        var params = {};
        $(this).serializeArray().map(function (x) {
            params[x.name] = x.value;
        });

        $.ajax({
            url: "/login",
            type: "post",
            data: params,
            success: function (resp) {
                errmsg = '<div class="error_tip" style="display: block">' + resp.errmsg + '</div>'
                $('.login_form').html('')
                if (resp.errno == 0) {
                    updateData(page_index)
                } else {
                    $('.login_form').html('')
                    var content = '<h1 class="login_title">用户登录</h1>' +
                        '<input type="text" name="username" placeholder="用户名" class="input_txt">' +
                        '<input type="password" name="password" placeholder="密码" class="input_txt">'
                    content += errmsg
                    content += '<input type = "submit" value = "登 录" class= "input_sub" >'
                    $(".login_form").append(content)
                }
            }
        })
    })
})

/**
 * 登出
 */
function logout() {
    $.ajax({
        url: "/logout",
        type: "post",
        success: function (resp) {
            location.reload()
        }
    })
}

/**
 * 删除内容
 */
function deletes(i) {
    $.ajax({
        url: "/delete/" + (i + (10 * (page_index - 1))),
        type: "post",
        success: function (resp) {
            if (resp.errno === 0) {
                updateData(page_index)
            } else {
                alert(resp.errmsg)
            }
        }
    })
}

/**
 * 更新页面
 */
function updateData(index = 1) {
    page_index = index
    $.get('/total', function (resp) {
        new Pagination({
            element: '#pages',
            type: 1,
            pageIndex: page_index,
            pageSize: 10,
            pageCount: 7,
            total: resp.data,
            jumper: true,
            singlePageHide: false,
            prevText: '上一页',
            nextText: '下一页',
            disabled: true,
            currentChange: function (index) {
                console.log(index);
                page_index = index
                updateData(index)
            }
        });
    })
    $.get('/get_data?index=' + index, function (resp) {
        if (resp) {
            $('.list_con').html('')
            for (var i = 0; i < resp.data.length; i++) {
                var news = resp.data[i]
                var del = '<input type = "button" onclick="deletes(' + i + ');" value = "删 除" class= "input_sub2">'
                if (resp.errno != "0") {
                    del = ""
                }
                var content = '<li>'
                content += '<div class="news_detail">' + news + '</div>'
                content += del
                content += '</li>'
                $(".list_con").append(content)
            }
            $('.login_form').html('')
            if (resp.errno == 0) {
                var content = '<input type = "button" onclick="logout();" value = "登 出" class= "input_sub" >'
                $(".login_form").append(content)
            } else {
                $('.login_form').html('')
                var content = '<h1 class="login_title">用户登录</h1>' +
                    '<input type="text" name="username" placeholder="用户名" class="input_txt">' +
                    '<input type="password" name="password" placeholder="密码" class="input_txt">'
                content += '<input type = "submit" value = "登 录" class= "input_sub" >'
                $(".login_form").append(content)
            }
            if (resp.data.length === 0 && page_index !== 1) {
                page_index = page_index - 1
                updateData(page_index)
            }
        }
    })
}
