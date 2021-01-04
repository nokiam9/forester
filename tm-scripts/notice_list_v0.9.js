// ==UserScript==
// @name         TM of notice list without content
// @namespace    www.caogo.cn
// @version      0.9
// @description  scrapy notice info from DOM
// @author       sj0225@icloud.com
// @match        https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=*
// @require      https://b2b.10086.cn/b2b/supplier/b2bStyle/js/jquery.min.js
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// ==/UserScript==

(function() {
    'use strict';

    // Func: 用于从指定页面开始爬取数据
    async function gotoPage(pageNumber){
        await waitForSelector(window, 'a.current'); // 等待‘当前页码’元素出现
        document.querySelector('#pageNumber').value = pageNumber; // 模拟输入‘页码’
        document.querySelector('#pageid2 > table > tbody > tr > td:nth-child(8) > input[type=button]').onclick(); //模拟点击‘GO’按钮
        await waitForSelector(window, 'a.current');

        let x = document.querySelector('a.current').innerText;
        if (Number(x) == pageNumber) {
            console.log('Test: 成功调转到断点页码， 当前页码=', x );
            await sleep(3000);
        }
        else {
            alert('严重错误: 无法调转到断点页码， 当前页码=' + x );
        }
    }

    // main主程序入口
    (async function main() {
        const active_page_selector = 'a.current';
        const first_notice_selector = '#searchResult > table > tbody > tr:nth-child(3)';
        const next_page_button_selector = '#pageid2 > table > tbody > tr > td:nth-child(4) > a';
        const content_base_url = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id=';
        const post_base_url = 'http://127.0.0.1:3000/api/notices/';

        const notice_type_id = window.location.search.split('=')[1]; // 取出url的参数值 [1,2,3,7,8,16]

        // 可能的初始化环节：填写页码数字，并模拟点击GO按钮，就可以跳转到指定页面
        //gotoPage(18);

        do {
            await waitForSelector(window, active_page_selector); // 提取当前活跃焦点的Page序号
            let page_now = Number(document.querySelector(active_page_selector).textContent);
            console.log('Info(main): page_now=', page_now, '，爬取&发送数据');

            let records = 0;
            let duplicated_records = 0;
            let line = document.querySelector(first_notice_selector); // 提取第一行notice
            while (line) {
                const nid = line.getAttribute('onclick').split("'")[1];
                const notice = {
                    spider: 'TM',
                    type_id: notice_type_id,
                    nid: nid,
                    source_ch: line.children[0].textContent,
                    notice_type: line.children[1].textContent,
                    title: line.children[2].children[0].textContent,
                    published_date: line.children[3].textContent,
                    notice_url: content_base_url + nid
                }; // 分析页面，获得公告列表的基础信息

                await postOneNotice(notice, post_base_url + nid).then( // 通过XHR发送爬取结果数据
                    response => {
                        if (response == 0) duplicated_records = 0; // 如果插入成功，重复量的计数器复位
                        else duplicated_records++;
                    },
                    error => { // post异常退出
                        console.log(error);
                        console.log('Error(main): XHR post failed, and exit...');
                        return -2;
                    }
                );

                records++;
                line = line.nextElementSibling; // 循环提取下一行
            };

            console.log('Debug: records=', records, ', dup_records=', duplicated_records);
            if (duplicated_records == records) { // 本页面全部记录重复，说明网站没有更新，正常退出
                console.log('Info(main): All records post duplicated, and exit...');
                return 0;
            }

            const next_page_btn = document.querySelector(next_page_button_selector); // 寻找‘下一页’按钮
            if (next_page_btn) {
                console.log('Info(main): Pause 5 seconds, then start to scrapy next page');
                next_page_btn.onclick(); // 模拟click动作
                await sleep(5000);
            }
            else { // 找不到‘下一页’的按钮，说明页面已全部提取
                console.log('Info(main): Scrapy data compeleted !!!');
                return -1;
            }
        } while(1);
    })();


    // Func: 向XHR发送公告数据
    function postOneNotice(notice, base_url){
        return new Promise((resolve, reject)=>{
            GM_xmlhttpRequest ({
                method:     "POST",
                url:        base_url + notice.nid,
                data:       JSON.stringify(notice),
                onload:     function (response){
                    if (response.status == 200) { // 插入成功
                        console.log('Insert record ok! nid=', notice.nid);
                        resolve(0);
                    }
                    else if (response.status == 405) { // 重复记录，约定http返回码=405
                        console.log('XHR onload info: Dup record found, nid=!', notice.nid);
                        resolve(-1);
                    }
                    else { // 未知应用错误
                        console.log('XHR onload error: Unknown error !!!');
                        reject(response);
                    }
                },
                onerror: function(error){ // POST网络故障时退出
                    console.log('XHR onerror: network error!');
                    reject(error);
                }
            });
        });
    }

    function waitForSelector(page, id){
        return new Promise((resolve, reject)=> {
            const retry_delay = 500;
            const retry_limits = 5;

            // console.log('Debug(waitforNode): start looking for node with ', selector_id);
            let retry_cnt = 0;
            setInterval(function myVar(){
                if (page.document.querySelector(id)) {
                    clearInterval(myVar);
                    resolve(page.document);
                } else if (retry_cnt >= retry_limits) {
                    clearInterval(myVar);
                    reject('Error(waitForSelector->myTimer): Failed searching for node=', id);
                } else retry_cnt++;
            }, retry_delay);
        })
    }

    function sleep(ms) {
        return new Promise((resolve) => {
            setTimeout(resolve, ms);
        });
    }
})();